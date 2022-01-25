const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const pk = modalBtn.getAttribute('data-pk')
    const title = modalBtn.getAttribute('data-quiz')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin <b>"${title}"</b>?</div>
        <div class="text-muted">
            <ul>
                <li>number of questions: <b>${numQuestions}</b></li>
                <li>time: <b>${time} min</b></li>
            </ul>
        </div>
    `

    startBtn.addEventListener('click', () => {
        window.location.href = pk
    })
}))