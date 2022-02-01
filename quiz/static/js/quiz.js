const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')
let timer

const activateTimer = (time) => {
    console.log(time)
    if (time.toString().length < 2) {
        timerBox.innerHTML = `Time left: <b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `Time left: <b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "Time left: <b>00:00</b>"
            setTimeout(() => {
                clearInterval(timer)
                alert('Time over.')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `Time left: <b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response) {
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans form-check-input" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        });
        activateTimer(response.time)
    },
    error: function(error) {
        console.log(error)
    }
})


const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const num_of_questions = document.getElementById('num_of_questions')
const return_btn = document.getElementById('return')
const see_res = document.getElementById('see_res')



const sendData = () => {
    const elements = [...document.getElementsByClassName('ans form-check-input')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response) {
            const results = response.results
            quizForm.classList.add('d-none')
            timerBox.remove()

            scoreBox.innerHTML = `Your result is: <b>${response.score.toFixed(2)}</b>%`

            results.forEach(res => {
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)) {
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp == 'not answered') {
                        resDiv.innerHTML += ' - not answered'
                        resDiv.classList.add('bg-danger')
                    } else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | answered: ${answer}`
                        }
                    }
                    resultBox.append(resDiv)
                }
            })
            return_btn.classList.remove('d-none')
            see_res.classList.remove('d-none')

        },
        error: function(error) {
            console.log(error)
            console.log(data)
        }
    })
}

quizForm.addEventListener('submit', e => {
    e.preventDefault()
    clearInterval(timer)
    sendData()
})