function toggleAnswer(questionId, answerId) {
    var question = document.getElementById(questionId);
    var answer = document.getElementById(answerId);
    question.style.display = 'none';
    answer.style.display = 'block';
}

function enable(next) {
    var nextBtn = document.getElementById(next);
    nextBtn.disabled = false;
}