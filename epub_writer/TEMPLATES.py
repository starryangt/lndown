from mako.template import Template

COVER = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Cover</title>
    <style type="text/css"> img { max-width: 100%; } </style>
  </head>
  <body>
      <img src="../Images/Cover.png" alt="cover"/>
  </body>
</html>
"""

PAGE_RAW = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
            <title>${title}</title>
    </head>
    <body>
        <h3>${title}</h3>
        ${body}
    </body>
</html>
"""

PAGE = Template(PAGE_RAW)


CONTENT_OPF_RAW = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="en">
   <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>${title}</dc:title> 

        <dc:creator id="creator01">${author}</dc:creator>
        <dc:language>en</dc:language>

        <meta property="dcterms:modified">2020-03-17T16:39:09Z</meta>

        % if publisher:
        <dc:publisher>${publisher}</dc:publisher>
        % endif

        % if date:
        <dc:date>2020-03-17</dc:date>
        % endif

        <dc:identifier id="pub-id">${UUID}</dc:identifier>
        <meta name="cover" content="Cover.jpg"/>
    </metadata>
    <manifest>
        <item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>
        <item id="Coverimg" href="Images/Cover.png" media-type="images/png"/>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="toc" href="Text/toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>

        % for element in epub_elements:
        <item id="${element.id}" href="${element.href}" media-type="${element.media}"/>
        % endfor
        
    </manifest>

    <spine toc="ncx" page-progression-direction="ltr">
        <itemref idref="cover"/>
        % for chapter in chapters:
        <itemref idref="${chapter.id}"/>
        % endfor
    </spine>
</package>
"""

CONTENT_OPF = Template(CONTENT_OPF_RAW)

TOC_RAW = """<?xml version="1.0" encoding="utf-8" ?>
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
  <head>
    <meta content="${UUID}" name="dtb:uid"/>
    <meta content="1" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>${title}</text>
  </docTitle>

  <navMap>
    <navPoint id="navPoint1">
      <navLabel>
        <text>Cover</text>
      </navLabel>
      <content src="Text/cover.xhtml"/>
    </navPoint>

    % for chapter in chapters:
    <navPoint id="navPoint${loop.index}">
        <navLabel>
            <text>${chapter.title}</text>
        </navLabel>
    <content src="${chapter.href}"/>
    </navPoint>
    % endfor
  </navMap>
</ncx>
"""

TOC = Template(TOC_RAW)

TOC_XHTML_RAW = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="default-style"/>
  <title>${title}</title>
  <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css"/>
</head>

<body>
  <nav epub:type="toc" id="toc"><h1 class="toc-title">Table of Contents</h1>

  <ol class="none" epub:type="list">
    <li class="toc-front"><a href="../Text/cover.xhtml">Cover</a></li>
    % for chapter in chapters:
    <li class="toc-front"><a href="${chapter.new_src()}">${chapter.title}</a></li>

"""

MIMETYPE = "application/epub+zip"

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
"""

DEFAULT_COVER_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAABYoSURBVHic7d17dBRVggbw73Z3jJKQpAMIJKHT6UBieIowO+MM4Oqo6+yoIA8RFBF56Poc5+w5io/ZXR97Zh0f6Ijo8cEjL8CZUWd2V8RRjw90BhgVZxATSNKBrECckIQYQjrprv1DUCRNcrtSVbeq+vv9oyRd1d9J9/3q1u3uagEThfJCo+CNThVAiSZEsUfDKA3IADAAQJaZ903kMC0A2gEchsBuaFqVJsQuTzT67p59+2rMulNh8P48oUDgfI/wzNc0XASBEQbvnygZ1QPaG0KI8j3h8LsAYkbt2JACOCs3d1B3SsqtWgzXc9ATmaoeEM93adGVe/fube7vzvpVAEU5RYOjKV13AbEbAJHe3zBEJO2w0PB0BLGH+1MEegtAFAYKFkBojwAYovfOiah/BHBI08Tymr11zwHQdGyfmFAoFBDRaDkgpiS6LRGZRbzZjdiC+vr6/QltlciNQ4HQpULE1gAYlMh2RGSJLyFwbU04vEl2A6/sDQsDBbcKoa0FkKYrGhGZLQ3APL8/q7G5pWW7zAYyBSBGBoO/BPAQjH/ZkIiM5RHApdlZ/lhza8u7fd24zwIYGQz+UtNwpzHZiMgi52dn+aN9lUCvBVCYX3ALvj7yE5HzXJCd5W9qbm3ZeqobnHJKPzJQcJkmtFd7uw0R2V4U0C6qqa9/O94v4w7ukbkj8zRf18eAGGxuNiKywMGowNnhcPjAyb/wxLmxR/N1VXLwE7nGUK+G1fF+0aMACgMFS/gmHyLXuWRkoODKk3/4nVOAvLy87FSvt4pHfyJXOqB5PWfV1ta2Hv/Bd2YAqd6Uuzn4iVxrmIhqt534g29mAF8f/X1hAAOtTkVE1hDAIe/pqcGqqqo24IQZwOk+323g4CdyNQ3I7j56dNnxfx8vAI8Ww/WKMhGRpcR3CyAUCF3AK/kQJY2i0IjQZOBYAXhEbJ7aPERkKU9sPnCsADTgQrVpiMhKAtpFACBCeaFRwhurVh2IiCylxTxiuAfe6FTVSYjIckLEYlN8Ap7ROq4lSEkkkJ+PzMwM+HwpqK6qQnt7u+pIZAABT4lPIFas8RO/dBIhBK6aNw/XXrcQo4qKvvl5JBLB65s24dFfPYKGffsUJqT+0hArFoX5wZ0ARqsOQ/aRlpaGx594Ahdc+ONT3uarr77CdQuuxScff2xhMjLYnzzgd/TRCdLT07F63dpeB//x2z3/4gsYEQhYlIxMkOkB3/5Lx6Snp2NN6TqcM2mS1O2z/H7cctutJqci82gDPeBlvgnAwIEDsaZ0Hc6eODGh7S6fPh0DB/IY4kxioAfxrwpESUTv4AeAlJQUFIQKTEhFFvBw8Ce5jIwMrC0rw4Szz9a9j5zcXAMTkZVYAEksIyMDq0vXYfyE8f3ajxB8GdmpfKoDkBoZGRlYU1ra78EPAJrGN5I5FWcAScjIwQ+AbyR1MBZAksnMzMTasjLjBj85Gk8BksjXg78UY8eNM3S/PAVwLhZAksjOzsa6inKcddZZhu+bBeBcLIAkkJ2djdKKChSfVWzK/lkAzsU1AJcbNGiQqYMfYAE4GWcALnZ88BcVF/V9437Q+DKAY3EG4FJWDX6AMwAnYwG40ODBg1FWac3gJ2fjKYDLHB/8I0eNsu5OOQNwLM4AXETJ4AfHv5OxAFxiyJAhSgY/wDUAJ+MpgAsMGz4MZRWVCBYEldz/tPPOw7Dhw3Rv33GkA5GuiCFZuiJdaGw8iJ07dyLaHTVkn24mCvODrG8HGz58OMoqK5EfzFcdxVZaWlpQtq4Uz65ahY6ODtVx7KqNBeBgOTk5KKusQCCfg/9UPtu5E4uuXYimpibVUeyojWsADpWbm4vy9ZUc/H0YPWYMnn72GXh48au4+FdxoOODn5fkljNp8mRcPmO66hi2xAJwmOPT/rwRI1RHcZTZc+aojmBLLAAHyc3NRcWG9Tzy6zB+/ATVEWyJBeAQIwIBVL60kUd+nQakDUBqaqrqGLbDAnCAvLw8lFaUIycnR3UUchkWgM0Fg0Gsf+kl5OXlqY5CLsR3AtpYMBhE+fpKDB2m/112RL3hDMCmCgoKOPgNxs8s9MQZgA0dH/xnDh2qOgq5HAvAZgoLC1FaWYEzzzxTdRRpjY2N6Dx6tNfbCI/HsG8R9vl8SEtL/Eut+RVmPbEAbCQUCqG0otxRgx8A/vWOn+ODLVssu78fnHsuyiorEt6OpwA9cQ3AJgoLC1HGab+pWAA9sQBswInTfnIHngIoVjhyJMoqKzBkyBDVUXTjqbVzcQagkBsGvwpczDMOC0CRkpISrN+4kYPfQlwD6IkFoEDJ6NFYV14Of7ZfdRRKclwDsFjJ6NEoLS9Dlt89g59TcufiDMBCo8eMcd3gV4GFYxwWgEVGjxmDdWWlHPwK8UtMe2IBWGDM2LFY5+ojP4/ITsUCMNmYsWOxtqwUWVlZqqMQ9cBFQBONHTcOpRXlhn0Ixq54Tu5cnAGYJG/ECDz34guuH/wq6O4bLgH0wAIwQZbfjxfXruGbfMj2WAAGS01NxXMvPI9QKKQ6imUccwrgkJhWYgEY7M7lyzHxnHNUx3A13YXDU4AeWAAGmjJ1ChYsvFZ1DCJpLACD+LP9ePjRR50zHU5C/DBQTywAgzzw0ENJe0EPp5SeU3JaiQVggB9N+REu+clPVMdIIvoGMmcAPbEA+snr8+Ke+36hOgaRLiyAfrpmwQIUFRepjqGUU6bWnAH0xALohyy/H7fefrvqGMo5pQCcktNKLIB+WLxkMT/kA+uPrHoHMmcAPbEAdEpLS8P8a65RHcMWeGR1LhaATvOuno/MzEzVMSgBnAH0xALQwefzYeGiRapjJC3OOIzDAtDh8unTMXz4cNUxbIPj0blYADrMmTtXdQQiQ7AAEpQ3YgQmf2+y6hhJjacAxmEBJGjW7Nl8Ap7MAX8PLgDGxwJIgBACM66YoToGkWFYAAk4e+JEjAgEVMewHc6InIsFkIBp552nOgKBhWMkFkACpp03TXUE0olrAPGxACRlZmZi7LhxqmMQGYoFIGnK1Knwer2qY9iS4OV2HYsFIGnSZL72T+7DApBUMrpEdQQ6Rs8iINcA4mMBSBBCoKi4WHUMIsOxACTk5OTwo7+9sPplOb4KaBwWgIRRRcl9zb++WF0AnM0bhwUg4cyhyXm9f1nWXxJMx0ZsjbhYABI4/e8d35nnXCwACRkZGaoj0IlYOIZhAUjI4AyAXIoFIGHAGQNUR7A1ngI4FwtAAp/gzsclwPhYABJYAPbCx8M4LAAZfL71igPSuVgAEvgEJ7diAUhgATgfPwwUHwtAAgugDxb/eXj9AeOwACSwAMitWAASeMQht2IBSOAMoHfWfxyYFwQxCgtAAguA3IoFIIPjn1yKBSCBM4De8e/jXCwACXyC2wvXAIzDApDAAiC3YgFIYAH0ji+TOhcLQAKf4ORWLAAJnAHYC9cAjMMCkMEC6BUL0rlYABL4/Ca3YgFI4BGO3IoFIIEF0Dt+FsC5WAASWADkViwACSwAcisWgAQWQO8s//vw4TAMC0AKn3GOxzWAuFgAEjgDILdiAUjg+Ce3YgFI4Aygd054GZDiYwFI4BPO+bgEEB8LQAILgNyKBSCBBdAH/nkciwUggQVgL3w8jMMCkMInHLkTC4D6zQlHZA1cBYyHBSDBCU/wZMJLtBmHBSCB4//Umg81Y9dnn1l6nzyaG4cFIIEzgPjCdWFcOWsWqj6vsvR+OQMwDgtAAgugp/ffew8zp09HXV2d6ihSeEGQ+FgAElgA37W+ohKLFy3C4cOHldw/Hw/j+FQHcAI+4b4W7e7GQw8+iHVr1qqOQgZhAchgAaC1tRW33nQzPtiyRXUUMhALQEKyLzrVh+uxbMkS1OzZozqKblwDiI9rABKS+RRg+7btmDNzpq0GfzI/HkZjAUhI1ufbxvUbcM28eTh06JDqKGQSngJISLYjTjQaxWOPPIJnVz2jOgqZjAUgIZkKoL29HXfcfjve+uObqqMYimsA8bEAJCRLATTs24eli5dgd3W16ii9SpbHwwpcA5CRBE+4j/7yF8yacYXtBz8ZiwUgwe1HnD/8/vdYMP9qNDU1qY5CFuMpgAS3vg9A0zT8+okn8eSKFaqjJIRfDmocFoAEN84AOo4cwc9/dgfe2LxZdRRSiAUgwW3j/+CBA7hh6TL87a9/VR2FFOMagAQ3zQB2fPIJZlx2OQc/AWABSHFLAbz2P/+Lq6+ahy+//FJ1lP7R8XBwDSA+FoAMhxeApml4dtUzuO2WW3D06FHVcchGuAYgwckzgM7OTtx951149ZVXVEchG2IBSHBqATQ2NuLGpUvx6Y5PVUchm2IBSHDi+wB27dqFGxYvwRdffKE6iuF0FTLXAOLiGoAEp80ANr32Gq6cNduVg5+MxQKQ4KTxv3b1Gtx28y3oOHJEdRRyAJ4CSHDCDCASieCe5cvx8m9/pzoKOQgLQILdC6D5UDNuuvFGbNu6VXUUS+j7LIAJQVyABSDDxgVQ9XkVbliyBA0NDaqjkANxDUCCXWcA777zDq6aM4eDn3RjAUiwYwGsXb0GS69fjLa2NtVRLOfEl2XtiqcAEuxUANHubtz/H/ejvLRUdRRyARaABLsccVpaWnDLv9yEP334oeoojsOvFI+PBSDBDhOAcF0YyxYvRm1treoo5CJcA5Cg+hTg/ffex8zp0zn4j1H9eLgJC0CGwifc+opKLFH4VdzkbjwFkKDiiBONRvGfDz6ItavXWH7fbsQLgsTHApBgdQG0t7fjZ7fehrffesvS+6XkwwKQYGUB7K2vx9LFzv4qbrNxDcA4XAOwke3btmP2Ffb6Km5yNxaABCuOOC9t2IAF8+fzq7hNwjWA+HgKIMGKNwLNmTsXc+bONf1+iE7EGYAEnnKSW7EAZLAByKVYABK46ux8XAOIjwUggQVAbsUCkMACILdiAVBS4ClAfCwACZwBOF/zoWbVEWyJBSCBBeB8n3z8seoItsQCkGCXKwKRPpqmYcP6StUxbIkFIIETAGcrXbuOX5B6CiwAGWwAx3pp40Y8eP/9qmPYFj8LIIFrAM4TrgvjyRUr8PtXX1UdxdZYABL0FMBjjzyKHZ9w4UmP2++4A+dMmqRr21gshqee/DVWrVyJrq4ug5O5DwtAgseT+JnSzr/9DVve32JCGnfL8vsxZuxYXdtqmoZ/u/c+VFZUGJzKvbgGIEHfl1HyjSd6zJo9G6mpqbq2XbVyJQd/glgAZBtCCMybP1/Xth9/9BGeeHyFwYncjwUgQc8SIGcAiRs3fhyCBcGEt4t2d+Puu5YjGo0ansntWAAyeApgifMv+LGu7V5++WXsrq42OE1yYAHI0DGY+dJh4r7/g+8nvI2maXhm5dMmpEkOLAAJHUePJrzNoMGDTEjiXl6vF2PHjkt4u+3btiEcDhsfKEmwACQcaW9PeJuhQ4eakMS9Bg8ZggFpAxLebtNrr5mQJnmwACQcPNiY8Db/8P3Ep7PJLDc3V9d2W//0Z4OTJBcWgITa2pqEtzn3hz9Eenq6CWncadCgxE+ZNE3D7t27TUiTPFgAEnZXJ/4kO+2007Bw0XXGh3EpPYumbW1t6O7uNiFN8mABSNj6Z33TzKU33IAhQ4YYnMad9Lxs2tnZaUKS5MICkPDpjh1o17EQmJ6ejqdWPY2UlBQTUrlLa2trwtsMHjwYp59+uglpkgcLQEJ3dzc2b3pd17aTJk/GYytW6H5/e7I4cOBAwtsIIVBcXGxCmuTBApD0ysu/073tT376z6jYuAEjAgEDE7nLgf37dZ3Pz5w9y4Q0yYMFIOnDDz7s19tNJ0yYgM1v/hH3/OI+5AfzDUzmDpFIBJ/v2pXwdjNmzkReXp4JiZKDKMwP8k3rkqZfMQOPPv64IfvaXV2NTz/9FPu/2I+OjiOIdEbQcbTDkH0fF4vF0NbWZug+AaD9q3ZEo8auvnd2dmLx0qW46OKLE95229ZteOiBB775d1vbYRzYf4CLhH1rYwEkwOvz4pU//AElJSWqo1AfIpEI3n/3PTz16yd5QdBTa/NmZ2X9u+oUTqHFNFR9/jlmXzmHH/axOa/Xi4JQCHPmzkVHRwc++stHqiPZUYQFkKD9+/cjIzMDEydOVB2FJAghMGXqVOzbt0/XGoPLRXgKoENKSgo2/OY3GD9hvOooJKmluRnnTzvPlDURB2vjqwA6dHV14cZly9DQ0KA6CknK8vvxT5dcojqG7bAAdGo8eBCLF16HpqYm1VFI0qTJ+i417mYsgH6oqanB3FmzORNwiCy/X3UE22EB9FM4HMaVM2dh29ZtqqNQHw41HVIdwXZYAAZobGzENfPnYdXKlYjy46m2tXUrLx5yMhaAQaLdUTz6q0dw+aWXYvu27arj0EkaGxux+fXNqmPYjgdATHUIN6n6vApXzZmDRdcuZBHYRCwWwy/uuRcdR46ojmI3MVGYHzwMYKDqJG41qqgIM2fNwkUXX6zrSy+ofzo7O3Hv3Xfj5d/q/zSne2kNojA/+H8AclRHSQY5OTmY/L3vYeSokQgVFsLv9yM9PR0ZGRn93ndaejq8Xq8BKb8lhDAkmwotzc14Y/NmrHp6FfbW16uOY1e7RGF+cCeA0aqTUPI47bTTcMYZZxi+3wEDBsCXkoLWlhYcPnzY8P270Ic+TaBGaCwAsk4kEkEkEjF8v3ouK5bctD0eoWlVqmMQkRJVHk2Iz1SnICLracAuj+j2vqc6CBFZTtM8ni2emoaaPQC4TEqUXP5aV1d38Ng7AbU31GYhImuJN4Bv3wpcoTAJEVlMIFbx9X+P/bswP1gLIKgsERFZZVdNfXg08O0MQNM0rFYYiIgsIgSeO/7/33waMBLrfgoAL5hG5G5Nqe1pPQugoaHhkBB4Wk0mIrKCgPbYzi93fnX839+5HkAkFvsvAI2WpyIi82nYl3ok/ckTf/Sdj4+1trYe9fuzmgQw3dpkRGQ2TWjXV3+xe8eJP4v39TaiMD/4FoB/tCQVEZlOQPvvPfX1l53883iXBNOiAvMAJP6F7URkQ1qDpyt1UbzfxL0mYDgcPgCBReDlwogcTuuOxTzzq7+o/nu8357yEjLNLS17/P6sLwXwU/PCEZGJNA1YVrc3/OqpbtDrNaSaW1q2Z2dl+gAxzfhsRGQmTcPy2r31T/V2mz4vItfc2vq2PzPrqBC40LhoRGQiTQjcX1MffqivG0pdRbK5tWXLoKzMvwPiEsR/5YCI7CEKTdxYUx9+TObGCQ3mwvz8CwBRDmCYrmhEZKbGmCauqdtbJ/3x/oS+Gaimvv4tXyw6CcDbCUcjIjNtgs87LpHBD+ifzovCQMECCO1hAEN17oOI+m8/NHFXzd66UgBaohvr/iaJ5taWHQMzM17wQMSEwAQAqXr3RUQJaxECD4sU39U1dbVb9e7EkAW9QCDgTxHemwFtCYB8I/ZJRHHVCoHn4fOt3LNnT7+//cToFX3PyGBwqqZpVwPiIvAKQ0RGqIWGzRo85bV7a7dAx1T/VEx9Sa8oEAhFPZ5pAEoQQzEEigBtICDSAWSZed9EDtMCaF8B4jCAaiFQpQG7osA74XA4bNad/j+hfaRdE5W+NgAAAABJRU5ErkJggg=="