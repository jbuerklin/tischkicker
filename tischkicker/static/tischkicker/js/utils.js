import { Tooltip } from './bootstrap.js'

/**
 * Retrieve and parse data from a Django json_script template tag
 *
 * @param {string} id - name of the json_script (`json_script:"id"`)
 * @returns {Array | object} parsed JSON object, or empty array
 */
export function getContextData(id) {
    if (!id) {
        return []
    }
    const node = document.querySelector(`#${id}`)
    if (node !== undefined) {
        try {
            return JSON.parse(node.innerText)
        } catch (error) {
            return []
        }
    }
    return []
}

/**
 * Initalize Bootstrap tooltips since they are not initialized by default
 *
 * @param {string} [selector] - selector for the tooltip elements
 */
export function initializeTooltips(selector = '[data-bs-toggle="tooltip"]') {
    document
        .querySelectorAll(selector)
        .forEach((element) => Tooltip.getOrCreateInstance(element))
}
