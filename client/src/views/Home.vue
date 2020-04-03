<template>
  <div class="home">
    <v-container>
      <v-row fluid>
        <v-col>
          <v-row>
            <v-expansion-panels
              accordion
            >
              <v-expansion-panel>
                <v-expansion-panel-header>More metadata</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-text-field
                    label="Publisher"
                    v-model="publisher"
                  ></v-text-field> 
                  <v-text-field
                    label="Filename"
                    v-model="filename"
                  ></v-text-field>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-row>
          <v-row>
            <v-text-field
              label="Title"
              v-model="title"
            ></v-text-field>
          </v-row>
          <v-row>
            <v-text-field
              label="Author"
              v-model="author"
            ></v-text-field>
          </v-row>
          
          <v-row>
            <v-select
            :items="scraper_items"
            label="Scraper"
            v-model="scraper"
            ></v-select>
          </v-row>
          <v-row>
            <v-select
            :items="parser_items"
            label="Parser"
            v-model="parser"
            ></v-select>
          </v-row>
          <v-row>
            <v-btn block v-on:click="compile">Compile</v-btn>
          </v-row>
          </br>
          <v-row>
            <v-btn block v-on:click="clear">Clear</v-btn>
          </v-row>

          <v-row fluid>
            <p>Paste URLs Here</p>
            <v-card
            outlined
            class="mx-auto"
            min-width="100%"
            min-height="200px"
            max-height="200px"
            style="overflow: scroll"
            >
              <draggable 
              v-model="urls" 
              group="people" 
              @start="drag=true" 
              @end="drag=false"
              tag="ul"
              >
                  <li v-for="element in urls" :key="element.id">{{element.title}} | <i>{{element.href}}</i></li>
              </draggable>
            </v-card>
          </v-row>
          <v-row>
            <p>Console</p>
            <v-card
                outlined
                class="mx-auto"
                min-width="100%"
                min-height="200px"
                max-height="200px"
                style="overflow: scroll"
                >
                </draggable>
              </v-card>

          </v-row>
          
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import draggable from 'vuedraggable'

import { eel } from './eel.js'

export default {
  name: 'Home',
  components: {
    draggable
  },
  data: () => ({
    title: '',
    author: '',
    cover: '',
    publisher: '',
    filename: '',
    scraper: 'http',
    parser: 'readability',
    urls: [],
    scraper_items: [
      'http'
    ],
    parser_items: [
      'readability',
      'dragnet'
    ]
  }),
  methods: {
    compile: function(){
      if (!this.urls){
        return
      }
      let metadata = {
        'title': this.title,
        'author': this.author,
        'publisher': this.publisher,
        'filename': this.filename,
        'scraper': this.scraper,
        'parser': this.paarser,
      }
      eel.compile(metadata, this.urls)
    },
    clear: function(){
      this.urls = []
    },
    handle_paste: function(e){
      e.stopPropagation()
      e.preventDefault()

      let clipboardData = e.clipboardData || window.clipboardData
      let pastedData = clipboardData.getData('text/html')

      let doc = new DOMParser().parseFromString(pastedData, 'text/html')
      let links = doc.querySelectorAll("a")

      for(let a of links){
        this.urls.push({
          'id': this.urls.length,
          'title': a.textContent,
          'href': a.getAttribute("href")
        })
      }
    }
  },
  mounted: function(){
    document.body.addEventListener('paste', this.handle_paste)
  }
}
</script>
