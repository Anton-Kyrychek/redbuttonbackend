(function main() {
    var audioElement = new Audio("data:audio/wav;base64," + music)
    var flag = false

    setTimeout(function (){
        var opt_sel = $('option:selected').get()
        for (let i = 0; i < opt_sel.length; i++) {
            if(opt_sel[i].outerText === 'активна') {
                flag = true
                break
            }
        }
        if (flag) {
            setInterval(function (){
                audioElement.play()
            },10000)}
        }, 1000)
    setTimeout(function (){
        document.location.reload()
    }, 100000)
})()
