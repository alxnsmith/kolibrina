class Question {
    constructor(author_id, category_id, theme_id, difficulty, question_text, correct_answer, answer2, answer3, answer4, pos) {
        this.author_id = author_id
        this.pos = pos
        this.category_id = category_id
        this.theme_id = theme_id
        this.difficulty = difficulty
        this.question = question_text
        this.correct_answer = correct_answer
        this.answer2 = answer2
        this.answer3 = answer3
        this.answer4 = answer4
    }
}

class QuestionList {
    constructor(quantity_questions, categories_and_themes = false) {
        this._list = {}
        this._quantity_questions = quantity_questions
        this._categories_and_themes = categories_and_themes
    }

    write_question(args) {
        if (args.pk && args.author_id && args.category_id && args.theme_id && args.difficulty && args.question_text && args.correct_answer && args.answer2 && args.answer3 && args.answer4 && args.pos) {
            this._list[args.pk] = new Question(args.author_id, args.category_id, args.theme_id, args.difficulty, args.question_text, args.correct_answer, args.answer2, args.answer3, args.answer4, args.pos)
            return true
        } else {
            return false
        }
    }

    get list() {
        return this._list
    }

    start_event_listener_for_circle_buttons(reader) {
        let questions = Array.from(document.querySelectorAll('.circle_btn'))
        questions.forEach(btn => {
            console.log(btn)
            btn.onclick = e => {
                console.log(e)
                let class_list = e.target.parentElement.classList
                if (!class_list.contains('act')) {
                    let question = reader()
                    if (question !== false) {
                        this.write_question(question)
                        this.visual_question_num_switcher(e)
                        if (class_list.contains('ok')) {
                            let dataset = e.target.parentElement.dataset
                            this.write_question_to_fields(this.get_question(dataset['rowNum'] + e.target.innerText))
                        }
                    } else {
                        show_modal_notification('Заполните все поля вопроса.')
                    }
                }
            }
        })
    }

    visual_question_num_switcher(e) {
        let current_question = document.querySelector('.act')
        let new_question = e.target
        current_question.classList.remove('act')
        current_question.classList.add('ok')
        new_question.parentElement.classList.add('act')
        this.clean_fields()
    }

    clean_fields() {
        if (this._categories_and_themes) {
            // Функцонал для заполнения полей категории и темы вопроса
            document.getElementById('category_id').value = ''
            document.getElementById('theme_id').value = ''
        }
        document.getElementById('question_text').value = ''
        document.getElementById('correct_answer').value = ''
        document.getElementById('answer2').value = ''
        document.getElementById('answer3').value = ''
        document.getElementById('answer4').value = ''
    }

    write_question_to_fields(question) {
        if (this._categories_and_themes) {
            // Функцонал для заполнения полей категории и темы вопроса
        }
        document.getElementById('question_text').value = question.question
        document.getElementById('correct_answer').value = question.correct_answer
        document.getElementById('answer2').value = question.answer2
        document.getElementById('answer3').value = question.answer3
        document.getElementById('answer4').value = question.answer4
    }

    get_question(pk) {
        return this._list[pk]
    }

    get quantity_questions(){
        return Object.keys(this._list).length
    }
    get enough_questions(){
        return this._quantity_questions
    }
    check_enough_questions() {
        return Object.keys(this._list).length === this._quantity_questions
    }
}
