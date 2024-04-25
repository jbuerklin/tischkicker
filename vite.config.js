import { defineConfig } from 'vite'
import { djangoVitePlugin } from 'django-vite-plugin'
import fs from 'fs'
import path from 'path'

const mode = process.env.APP_ENV

/**
 * Searches through the project's HTML files and extracts the entrypoints from the {% vite %} tag.
 *
 * @returns {Array<string>} list of entrypoints
 */
const findEntrypoints = () => {
  let folders = ['.']
  let files = []
  while (folders.length > 0) {
    const folder = folders.pop()
    if (
      ['node_modules', 'venv', 'vite_build', 'static'].includes(
        path.basename(folder)
      )
    ) {
      continue
    }
    let results
    try {
      results = readDirectory(folder)
    } catch (error) {
      continue
    }
    files = files.concat(results.files)
    folders = folders.concat(results.folders)
  }
  const entrypoints = new Set()
  for (const file of files) {
    if (file.endsWith('.html')) {
      const content = fs.readFileSync(file, 'utf8')

      const viteTags = content.matchAll(/{%\s+vite\s+.*?%}/g)

      for (const tag of viteTags) {
        const matches = tag[0].matchAll(/\s+('|")(.+?)\1\s+/g)
        for (const match of matches) {
          entrypoints.add(match[2])
        }
      }
    }
  }
  const entrypointsList = Array.from(entrypoints)
  console.log(`found entrypoints:\n${entrypointsList.join('\n')}`)
  return entrypointsList
}

/**
 * Parses the given directory and extracts a list of all files and all subdirectories.
 *
 * @typedef ReadDirectoryReturnObject
 * @property {Array<string>} folders - list of all subdirectories
 * @property {Array<string>} files - list of all files
 * @param {string} dirPath - directory path to read
 * @returns {ReadDirectoryReturnObject} two list; all files and all subdirectories
 */
const readDirectory = (dirPath) => {
  const data = fs.readdirSync(dirPath)
  const folders = []
  const files = []
  data.forEach((file) => {
    const filepath = path.join(dirPath, file)
    if (file.includes('.')) {
      files.push(filepath)
    } else {
      folders.push(filepath)
    }
  })
  return { folders, files }
}

export default defineConfig({
  plugins: [
    djangoVitePlugin({
      input: findEntrypoints(),
      addAliases: true,
      reloader: (fileName) => fileName.endsWith('.html'),
      delay: 500
    })
  ],
  build: {
    minify: 'esbuild'
  },
  resolve: {
    alias: {
      '@node_modules_static': (mode === 'local') ? path.resolve(__dirname, 'static') : path.resolve(__dirname, 'node_modules'),
      '@node_modules': path.resolve(__dirname, 'node_modules')
    }
  }
})
