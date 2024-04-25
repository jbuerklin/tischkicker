// this creates a minified module that can be imported in other files without having to bundle bootstrap in every file
import 'vite/modulepreload-polyfill'
export * from 'bootstrap'
