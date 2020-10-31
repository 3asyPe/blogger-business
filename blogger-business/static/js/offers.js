saw_help = localStorage.getItem('blogger-help')

if (!saw_help){
    $("#myModal").modal()
    localStorage.setItem('blogger-help', true)
}