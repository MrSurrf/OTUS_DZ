// Загрузка правил при загрузке страницы
document.addEventListener("DOMContentLoaded", loadRules)

// Функция загрузки правил
function loadRules() {
  fetch("/get_rules")
    .then((response) => response.json())
    .then((data) => {
      console.log("Текущие правила:", data)
      document.getElementById("rulesContainer").innerText = JSON.stringify(data, null, 2)
    })
    .catch((error) => console.error("Ошибка загрузки правил:", error))
}

// Функция отправки нового правила
function submitRule() {
  const formData = new FormData(document.getElementById("ruleForm"))
  const formDataObj = Object.fromEntries(formData)

  fetch("/apply_rule", {
    method: "POST",
    body: JSON.stringify(formDataObj),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message)
      // Перезагрузка правил после успешного добавления
      loadRules()
    })
    .catch((error) => console.error("Ошибка:", error))
}

