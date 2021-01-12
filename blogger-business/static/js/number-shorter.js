function toShortenNumber(number){
    function abbreviate(number, maxPlaces) {
        number = Number(number)
        var abbr
        if(number >= 1e9) {
          abbr = 'B'
        }
        else if(number >= 1e6) {
          abbr = 'M'
        }
        else if(number >= 1e3) {
          abbr = 'K'
        }
        else {
          abbr = ''
        }
        return annotate(number, maxPlaces, abbr)
      }
      
      function annotate(number, maxPlaces, abbr) {
        // set places to false to not round
        var rounded = 0
        switch(abbr) {
            case 'B':
                rounded = number / 1e9
                break
            case 'M':
                rounded = number / 1e6
                break
            case 'K':
                rounded = number / 1e3
                break
            case '':
                rounded = number
                break
        }
        if(maxPlaces !== false) {
            var test = new RegExp('\\.\\d{' + (maxPlaces + 1) + ',}$')
            if(test.test(('' + rounded))) {
                rounded = rounded.toFixed(maxPlaces)
            }
        }
        return rounded + abbr
    }
    return abbreviate(number, 1)
}

function parseShortenNumber(number){
    strNumber = number.toString()
    number = parseInt(number)
    abbr = strNumber[strNumber.length - 1]
    switch(abbr) {
        case "b":
        case 'B':
            number = number * 1e9
            break
        case "m":
        case 'M':
            number = number * 1e6
            break
        case "k":
        case 'K':
            number = number * 1e3
    }
    return number
}
