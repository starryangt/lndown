from bs4 import BeautifulSoup
from uuid import uuid4
from pathlib import Path
import shutil
from epub_writer import TEMPLATES as t
import shutil
import aiofiles
import aiohttp
import asyncio
import os
import zipfile
import base64

class EPuB:
    '''
    Main class
    Takes in metadata + list of HTML content in constructor
    `compile` method writes files to a temporary directory,
    downloads (or copies) any <img> tags in the HTML content
    Zips it up and produces a file
    '''

    def __init__(self, metadata, content):
        '''
        Metadata is a dictionary
            * title 
            * author
            * publisher
            * cover

        Content is a list of dictionaries
            * title 
            * html

        '''

        self.title = metadata.get('title', '')
        self.author = metadata.get('author', '')
        self.publisher = metadata.get('publisher', '')
        self.cover = metadata.get('cover', '')
        self.filename = metadata.get('filename', '')
        if not self.filename:
            self.filename = self.title
            if not self.title:
                self.filename = "untitled"
        self.UUID = str(uuid4())


        self.images = []
        self.chapters = []
        for item in content:
            #some parsing has to be done; we need to make sure all images are 
            #downloaded
            soup = BeautifulSoup(item.get('html', ''), 'html.parser')
            for img in soup.find_all('img'):
                src = img['src']
                image = Image(src)
                img['src'] = image.new_src()
                self.images.append(image)

            #then we just stick it in the mako template
            html_string = t.PAGE.render(title=item.get('title', ''), body=soup.prettify()) 

            chapter = Chapter(html_string, item.get('title', ''))
            self.chapters.append(chapter)

        
    #TODO: Error checking for both
    async def write_chapters(self, tmp_dir):
        for chapter in self.chapters:
            full_dir = tmp_dir / chapter.filepath()
            async with aiofiles.open(str(full_dir), 'w') as f:
                await f.write(chapter.HTML)
    
    async def write_images(self, tmp_dir):
        async with aiohttp.ClientSession() as session:
            for image in self.images:
                full_dir = tmp_dir / image.filepath()
                async with session.get(image.src) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(str(full_dir), 'wb') as f:
                            await f.write(await resp.read())
    
    async def async_compile(self, tmp_dir, output_dir):
        #first, make the file structure for the temp directory
        full_dir = tmp_dir / 'tmp'
        if full_dir.exists():
            if full_dir.is_dir():
                shutil.rmtree(str(full_dir))
        full_dir.mkdir(parents=True)
        
        #EPuBs have the following structure
        #Root
        # mimetype
        # -> OEBPS
        #   -> Text
        #   -> Images
        #   -> content.opf
        #   -> toc.ncx
        # -> META-INF
        #   -> container.xml

        OEBPS = (full_dir / 'OEBPS')
        META = (full_dir / 'META-INF')
        
        TEXT = (OEBPS / 'Text')
        IMAGES = (OEBPS / 'Images')

        OEBPS.mkdir()
        META.mkdir()

        TEXT.mkdir()
        IMAGES.mkdir()

        #with the cool folders and shit, we can now start writing files

        #MIMETYPE
        with open(str(full_dir / 'mimetype'), 'w') as f:
            f.write(t.MIMETYPE)

        #content.opf
        with open(str(OEBPS / 'content.opf'), 'w') as f:
            f.write(t.CONTENT_OPF.render(
                title=self.title,
                author=self.author,
                UUID=self.UUID,
                epub_elements=self.chapters + self.images,
                chapters=self.chapters
            ))

        with open(str(OEBPS / 'toc.ncx'), 'w') as f:
            f.write(t.TOC.render(
                UUID=self.UUID,
                title=self.title,
                chapters=self.chapters
            ))
 
        with open(str(TEXT / 'cover.xhtml'), 'w') as f:
            f.write(t.COVER)

        #is there a cover? In that case, we make a special Image object for it
        if self.cover:
            cover_image = Image(self.cover)
            cover_image.UUID = 'Cover'

            self.images.append(cover_image)
        else:
            with open(str(IMAGES / 'Cover.png'), 'wb') as f:
                cover = base64.b64decode(t.DEFAULT_COVER_IMAGE)
                f.write(cover)

        #chapter xhtml files
        await self.write_chapters(full_dir)

        await self.write_images(full_dir) 

        result_file = output_dir / (self.filename + '.epub')

        #can't just zip up the directory, because mimetype MUST be first
        #THEN META-INF
        def write_dir(path, zip, arcpath):
            for root, dirs, files in os.walk(path):
                for file in files:
                    zip.write(os.path.join(root, file), arcname=os.path.join(arcpath, file))


        with zipfile.ZipFile(str(result_file), 'w', zipfile.ZIP_STORED) as zipf:
            zipf.writestr("mimetype", t.MIMETYPE)
            zipf.writestr("META-INF/container.xml", t.CONTAINER)
            zipf.write(OEBPS / 'content.opf', arcname="OEBPS/content.opf")
            zipf.write(OEBPS / 'toc.ncx', arcname="OEBPS/toc.ncx")

            write_dir(IMAGES, zipf, "OEBPS/Images/")
            write_dir(TEXT, zipf, "OEBPS/Text/")

        #shutil.make_archive(str(result_file), 'zip', str(full_dir))

        shutil.rmtree(full_dir)
        


    def compile(self, tmp_dir, output_dir):
        asyncio.run(self.async_compile(tmp_dir, output_dir))

class EPuBItem:

    def __init__(self, id, href, media):
        self.id = id
        self.href = href
        self.media = media

class Chapter(EPuBItem):
    '''
    Represents a chapter in the epub
    Has an HTML string, and a UUID
    UUID represents final path
    '''

    def __init__(self, HTML, title = ''):
        self.HTML = HTML
        self.UUID = str(uuid4())
        self.title = title
        super().__init__(self.UUID, f'Text/{self.UUID}.xhtml', 'application/xhtml+xml')
    
    def new_src(self):
        return f'../Text/{self.UUID}.xhtml'
    
    def filepath(self):
        return Path('OEBPS/Text') / Path(f'{self.UUID}.xhtml')

    def __str__(self):
        return f'...{self.HTML[:20]}... | {self.UUID}'
    
    def __repr__(self):
        return str(self)

class Image(EPuBItem):
    '''
    Represents an image in HTML content

    Needs to a do a few things:
    * Keep track of the URL (if it is a URL), so it can be downloaded later
    * Download that image (or copy, if it is a filesys path)
    * Creates a UUID that is used as the file name
    * Return the new <img> tag
    '''

    def __init__(self, URL):
        self.src = URL
        self.UUID = str(uuid4())
        super().__init__(self.UUID, f'Images/{self.UUID}.png', 'image/png')

    def new_src(self):
        return f'../Images/{self.UUID}.png'
    
    def filepath(self):
        return Path('OEBPS/Images') / Path(f'{self.UUID}.png')
    
    def __str__(self):
        return f'{self.new_src()} | {self.src}'
    
    def __repr__(self):
        return str(self)