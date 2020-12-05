var applicationsCountHtml = document.querySelector(".nav-applications-count")

fetch("/api/applications/count/")
.then(response => {
    return response.json()
})
.then(data => {
    applicationsCountHtml.innerHTML = data.applications_count + " new "
})