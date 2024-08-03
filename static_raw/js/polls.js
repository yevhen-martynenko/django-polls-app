document.addEventListener("DOMContentLoaded", function () {
    const addQuestionBtn = document.getElementById("add-question");
    const makePrivateBtn = document.getElementById("make-private");
    const questionsContainer = document.getElementById("questions-container");

    if (addQuestionBtn && questionsContainer) {
        addQuestionBtn.addEventListener("click", function () {
            const questionDiv = document.createElement("div");
            questionDiv.classList.add("question");
            const mainDiv = document.createElement("div");
            mainDiv.classList.add("question__main");
            const footerDiv = document.createElement("div");
            footerDiv.classList.add("question__footer");

            const questionInput = document.createElement("input");
            questionInput.type = "text";
            questionInput.name = "question_text";
            questionInput.classList.add("question__input");
            questionInput.placeholder = "Question text";
            questionInput.required = true;
            mainDiv.appendChild(questionInput);

            const questionSelect = document.createElement("select");
            questionSelect.name = "question_type";
            questionSelect.classList.add("question__select");
            const types = ["Short Text", "Long Text", "Checkbox", "Radio"];
            types.forEach(function (type) {
                const option = document.createElement("option");
                option.value = type.toUpperCase();
                option.textContent = type;
                questionSelect.appendChild(option);
            });
            mainDiv.appendChild(questionSelect);

            const deleteQuestionBtn = document.createElement("button");
            deleteQuestionBtn.type = "button";
            deleteQuestionBtn.classList.add("question__delete-button", "default-button");
            deleteQuestionBtn.textContent = "Delete Question";
            deleteQuestionBtn.addEventListener("click", function () {
                questionDiv.remove();
            });
            footerDiv.appendChild(deleteQuestionBtn);

            const requiredDiv = document.createElement("div");
            const requiredLabel = document.createElement("label");
            const requiredCheckbox = document.createElement("input");
            const requiredLabelText = document.createElement("span");
            const questionIndex = Array.from(questionsContainer.children);
            requiredDiv.classList.add("question__required-container", "default-button");
            requiredLabel.classList.add("question__required-label");
            requiredCheckbox.classList.add("default-checkbox");
            requiredLabelText.classList.add("question__required-text");
            requiredCheckbox.type = "type";
            requiredCheckbox.type = "checkbox";
            requiredCheckbox.name = "required" + questionIndex.length;
            requiredCheckbox.value = true;
            requiredLabelText.textContent = "Required";
            requiredLabel.appendChild(requiredLabelText);
            requiredLabel.appendChild(requiredCheckbox);
            requiredDiv.appendChild(requiredLabel);
            footerDiv.appendChild(requiredDiv);
            
            const optionsContainer = document.createElement("div");
            optionsContainer.classList.add("options");
            optionsContainer.style.display = "none";

            const addOptionBtn = document.createElement("button");
            addOptionBtn.type = "button";
            addOptionBtn.classList.add("options__add-button", "default-button");
            addOptionBtn.textContent = "Add Option";
            optionsContainer.appendChild(addOptionBtn);

            questionDiv.appendChild(mainDiv);
            questionDiv.appendChild(optionsContainer);
            questionDiv.appendChild(footerDiv);

            questionsContainer.appendChild(questionDiv);
        });

        questionsContainer.addEventListener("change", function (event) {
            const target = event.target;
            if (target.classList.contains("question__select")) {
                const optionsContainer = target.closest(".question").querySelector(".options");
                if (target.value === "CHECKBOX" || target.value === "RADIO") {
                    optionsContainer.style.display = "flex";
                } else {
                    optionsContainer.style.display = "none";
                }
            }
        });

        questionsContainer.addEventListener("click", function (event) {
            if (event.target.classList.contains("options__add-button")) {
                const optionContainer = document.createElement("div");
                const optionInput = document.createElement("input");
                const deleteOptionBtn = document.createElement("button");
                const optionsContainer = event.target.closest(".question").querySelector(".options");
                const questionDiv = optionsContainer.closest(".question");
                const questionIndex = Array.from(questionsContainer.children).indexOf(questionDiv);
                optionContainer.classList.add("options__container");
                deleteOptionBtn.textContent = "Delete Option";
                deleteOptionBtn.classList.add("options__delete-button");
                deleteOptionBtn.setAttribute("type", "button");
                optionInput.name = "options_" + questionIndex;
                optionInput.type = "text";
                optionInput.classList.add("options__option");
                optionInput.placeholder = "Option text";
                optionContainer.appendChild(optionInput);
                optionContainer.appendChild(deleteOptionBtn);
                optionsContainer.appendChild(optionContainer);
                setTimeout(() => {
                    optionContainer.classList.add("option-active");
                }, 10); 
            }
            if (event.target.classList.contains("options__delete-button")) {
                event.stopPropagation();
                const optionContainer = event.target.closest("div");
                optionContainer.classList.add("option-disactive");
                setTimeout(() => {
                    optionContainer.remove();
                }, 300);
            }
        });
    }

    if (makePrivateBtn) {
        makePrivateBtn.addEventListener("click", function () {
            const publicContainer = document.getElementById("public-data");
            if (publicContainer.classList.contains("active")) {
                const inputFields = publicContainer.querySelectorAll("input");
                inputFields.forEach(input => {
                    input.value = "";
                });
            }
            publicContainer.classList.toggle("active");
        });
    }
});


// textarea autogrow
function autogrow(textarea) {
    textarea.style.overflow = "hidden";

    function update() {
        textarea.style.height = "1.5em";
        textarea.style.height = textarea.scrollHeight + "px";
    }

    textarea.addEventListener("input", update);
    window.addEventListener("load", update);
    window.addEventListener("resize", update);
}

const textareas = document.querySelectorAll(".wrap-textarea");

textareas.forEach(function(textarea) {
    autogrow(textarea);
});
