import { getContextData, initializeTooltips } from '@s:tischkicker/js/utils'

document.addEventListener('DOMContentLoaded', () => {
  initializeTooltips()
})

document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', (e) => {
    form.querySelectorAll('[type=submit]', (button) => {
      button.disabled = true
      setTimeout(() => { button.disabled = false }, 5000)
    })
  })
})

document.querySelectorAll('.debt_double').forEach(link => {
  link.addEventListener('click', (e) => {
    link.disabled = true
  })
})

document.querySelector('#toggleDoneDebts').addEventListener('click', (e) => {
  document.querySelectorAll('#debtTable .table-success').forEach(debt => {
    debt.classList.toggle('d-none')
  })
})
