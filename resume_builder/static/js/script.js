// static/js/script.js

// Add event listener to dynamically add work experience fields
document.addEventListener('DOMContentLoaded', function() {
    // Function to add a new work experience form
    function addWorkExperienceForm() {
        const workExperienceContainer = document.querySelector('#work-experience-container');
        const newFormIndex = workExperienceContainer.children.length; // Simple index for now

        // Create card element
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3');

        // Create card body
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        // Create form HTML (simplified, adjust based on your actual form structure)
        let formHTML = `
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-title">Title</label>
                <input type="text" class="form-control" id="work_experience-${newFormIndex}-title" name="work_experience-${newFormIndex}-title">
            </div>
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-company">Company</label>
                <input type="text" class="form-control" id="work_experience-${newFormIndex}-company" name="work_experience-${newFormIndex}-company">
            </div>
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-location">Location</label>
                <input type="text" class="form-control" id="work_experience-${newFormIndex}-location" name="work_experience-${newFormIndex}-location">
            </div>
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-start_date">Start Date</label>
                <input type="text" class="form-control" id="work_experience-${newFormIndex}-start_date" name="work_experience-${newFormIndex}-start_date">
            </div>
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-end_date">End Date</label>
                <input type="text" class="form-control" id="work_experience-${newFormIndex}-end_date" name="work_experience-${newFormIndex}-end_date">
            </div>
            <div class="form-group">
                <label for="work_experience-${newFormIndex}-description">Description</label>
                <textarea class="form-control" id="work_experience-${newFormIndex}-description" name="work_experience-${newFormIndex}-description" rows="3"></textarea>
            </div>
        `;

        cardBody.innerHTML = formHTML;
        card.appendChild(cardBody);
        workExperienceContainer.appendChild(card);
    }

    // Add event listener to the "Add Work Experience" button (if you have one)
    const addWorkExperienceButton = document.querySelector('#add-work-experience'); // Replace with your button's ID
    if (addWorkExperienceButton) {
        addWorkExperienceButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            addWorkExperienceForm();
        });
    }

    // Function to add a new education form
    function addEducationForm() {
        const educationContainer = document.querySelector('#education-container');
        const newFormIndex = educationContainer.children.length; // Simple index for now

        // Create card element
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3');

        // Create card body
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        // Create form HTML (simplified, adjust based on your actual form structure)
        let formHTML = `
            <div class="form-group">
                <label for="education-${newFormIndex}-institution">Institution</label>
                <input type="text" class="form-control" id="education-${newFormIndex}-institution" name="education-${newFormIndex}-institution">
            </div>
            <div class="form-group">
                <label for="education-${newFormIndex}-degree">Degree</label>
                <input type="text" class="form-control" id="education-${newFormIndex}-degree" name="education-${newFormIndex}-degree">
            </div>
            <div class="form-group">
                <label for="education-${newFormIndex}-major">Major</label>
                <input type="text" class="form-control" id="education-${newFormIndex}-major" name="education-${newFormIndex}-major">
            </div>
            <div class="form-group">
                <label for="education-${newFormIndex}-graduation_date">Graduation Date</label>
                <input type="text" class="form-control" id="education-${newFormIndex}-graduation_date" name="education-${newFormIndex}-graduation_date">
            </div>
            <div class="form-group">
                <label for="education-${newFormIndex}-description">Description</label>
                <textarea class="form-control" id="education-${newFormIndex}-description" name="education-${newFormIndex}-description" rows="3"></textarea>
            </div>
        `;

        cardBody.innerHTML = formHTML;
        card.appendChild(cardBody);
        educationContainer.appendChild(card);
    }

    // Add event listener to the "Add Education" button (if you have one)
    const addEducationButton = document.querySelector('#add-education'); // Replace with your button's ID
    if (addEducationButton) {
        addEducationButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            addEducationForm();
        });
    }

    // Function to add a new skill form
    function addSkillForm() {
        const skillsContainer = document.querySelector('#skills-container');
        const newFormIndex = skillsContainer.children.length; // Simple index for now

        // Create card element
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3');

        // Create card body
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        // Create form HTML (simplified, adjust based on your actual form structure)
        let formHTML = `
            <div class="form-group">
                <label for="skills-${newFormIndex}-skill">Skill</label>
                <input type="text" class="form-control" id="skills-${newFormIndex}-skill" name="skills-${newFormIndex}-skill">
            </div>
            <div class="form-group">
                <label for="skills-${newFormIndex}-level">Level</label>
                <input type="text" class="form-control" id="skills-${newFormIndex}-level" name="skills-${newFormIndex}-level">
            </div>
        `;

        cardBody.innerHTML = formHTML;
        card.appendChild(cardBody);
        skillsContainer.appendChild(card);
    }

    // Add event listener to the "Add Skill" button (if you have one)
    const addSkillButton = document.querySelector('#add-skill'); // Replace with your button's ID
    if (addSkillButton) {
        addSkillButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            addSkillForm();
        });
    }
});
