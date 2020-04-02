<template>
  <div class="home">
    <v-container>
      <v-col fluid>
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
      </v-col>
      <v-col fluid>
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
            <draggable v-model="urls" group="people" @start="drag=true" @end="drag=false">
                <div v-for="element in urls" :key="element.title">{{element.title}}</div>
            </draggable>
          </v-card>
        </v-row>
      </v-col>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import draggable from 'vuedraggable'

//import { eel } from './eel.js'

export default {
  name: 'Home',
  components: {
    draggable
  },
  data: () => ({
    title: '',
    author: '',
    cover: '',
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
    handle_paste: function(e){
      e.stopPropagation()
      e.preventDefault()

      let clipboardData = e.clipboardData || window.clipboardData
      let pastedData = clipboardData.getData('text/html')

      let doc = new DOMParser().parseFromString(pastedData, 'text/html')
      let links = doc.querySelectorAll("a")

      for(let a of links){
        this.urls.push({
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
