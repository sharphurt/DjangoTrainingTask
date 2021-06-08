let user
let cycle
let boosts = []

let autoClickInterval

function callClick() {
    cycle['coins_count'] += cycle['click_power']
    drawCycle()
    setAllBoostsAvailability()
}

function callAutoClick() {
    cycle['coins_count'] += 1
    drawCycle()
    setAllBoostsAvailability()
}


async function getUser(id) {
    let response = await fetch('/users/' + id, {
        method: 'GET'
    });
    user = await response.json();

    document.getElementById("user").innerHTML = user['username'];
    loadCycle().then(() => {
        drawCycle()
        loadBoosts().then(() => {
            drawBoosts()
        })
        setAutoClick()
        set_send_coins_interval()
    })
}

async function loadCycle() {
    let getCycle = await fetch('/cycles/' + user['cycle'], {
        method: 'GET'
    });
    cycle = await getCycle.json();

}

async function loadBoosts() {
    let boost_request = await fetch('/boosts/' + user.cycle, {
        method: 'GET'
    })
    boosts = await boost_request.json()
}

function drawCycle() {
    document.getElementById("data").innerHTML = cycle['coins_count'];
    document.getElementById("click_power").innerHTML = cycle['click_power'];
    document.getElementById("auto_click_power").innerHTML = cycle['auto_click_power'].toFixed(2);
}


function drawBoosts() {
    let parent = document.getElementById('boost-wrapper')
    parent.innerHTML = ''
    boosts.forEach(boost => {
        drawBoost(parent, boost)
    })
}

function buyBoost(name) {
    const csrfToken = getCookie('csrftoken')
    updateCoins().then(() => {
        fetch('/buy_boost/', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                boost_name: name
            })
        }).then(response => {
            if (response.ok) {
                loadCycle().then(() => drawCycle())
                loadBoosts().then(() => {
                    drawBoosts()
                    setAllBoostsAvailability()
                })
                setAllBoostsAvailability()
                setAutoClick()
                drawCycle()
            } else {
                return Promise.reject(response)
            }
        })
    })

}

function getInnerHTML(boost) {
    return boost.state ? `
        <div class="boost-holder" id="boost-holder-${boost.id}">
            <input id="buy" type="image" class="catgirl boost-button"
             src=""
              onclick="buyBoost(\'${boost.name}\')" />
            <div class="boost-info">
                <div class="name-info">
                    <div class="name" id="name"> ${boost.name} </div>
                    <div class="description" id="description"> ${boost.description} </div>
                </div> 
                <div class="price" id="boostPrice"> ${boost.price} </div>
            </div>
        </div>`.replace('src=""', 'src="' + staticImagesUrl + `${boost.name}.jpg"`)
        : `<div id="boost-holder-${boost.id}"> тут типа плейсхолдер для буста, который еше</div>`;
}


function drawBoost(parent, boost) {
    const div = document.createElement('div')
    div.setAttribute('class', `boost boost-type-${boost.type} boost-state-${boost.state}`)
    div.innerHTML = getInnerHTML(boost)
    parent.appendChild(div)
    setBoostAvailability(boost)
}


function setAllBoostsAvailability() {
    for (let boost of boosts)
        setBoostAvailability(boost)
}


function setBoostAvailability(boost) {
    const element = document.getElementById(`boost-holder-${boost.id}`).querySelector('#buy')
    const price = boost.price
    if (parseInt(price) > parseInt(cycle.coins_count))
        element.setAttribute('disabled', 'true')
    else
        element.removeAttribute('disabled')
}


function setAutoClick() {
    if (autoClickInterval)
        clearInterval(autoClickInterval)
    if (cycle['auto_click_power'] === 0)
        autoClickInterval = 0
    else
        autoClickInterval = setInterval(function () {
            callAutoClick()
        }, 1000 / cycle['auto_click_power'])
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function updateCoins() {
    const csrftoken = getCookie('csrftoken')

    return await fetch('/set_main_cycle/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            coins_count: cycle.coins_count,
        })
    })
}

function set_send_coins_interval() {
    setInterval(function () {
        updateCoins().then(response => {
            if (response.ok) {
                return response.json()
            } else {
                return Promise.reject(response)
            }
        }).then(data => {
            console.log(data['needToUpdate'])
            if (data['needToUpdate'] === true)
                loadBoosts().then(() => {
                    drawBoosts()
                    setAllBoostsAvailability()
                })
        }).catch(err => console.log(err))

    }, 2000)
}
