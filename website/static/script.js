
const wrapper = document.querySelector(".wrapper");
const selectBtn = wrapper.querySelector(".select-btn");
const selectedMovieInput = document.getElementById("selectedMovie");
const searchInput = document.getElementById("searchInput");
const optionsList = document.querySelector(".options");

selectBtn.addEventListener("click", () => {
    wrapper.classList.toggle("active");
});




// Function to filter the options based on search input
function filterOptions(searchText) {
    const options = document.querySelectorAll(".options li");
    options.forEach(option => {
        const optionText = option.textContent.toLowerCase();
        const isVisible = optionText.includes(searchText.toLowerCase());
        option.style.display = isVisible ? "block" : "none";
    });
}


function selectMovie(movie) {
    const trimmedMovie = movie.trim();
    
    // Set the trimmed movie as the input value
    selectedMovieInput.value = trimmedMovie;
    selectBtn.querySelector("span").textContent = movie; // Update the .select-btn span text here
    wrapper.classList.remove("active");
}





searchInput.addEventListener("input", () => {
    filterOptions(searchInput.value);
});


document.addEventListener("click", event => {
    const targetElement = event.target;
    if (!wrapper.contains(targetElement) && targetElement !== searchInput) {
        // Clicked outside the dropdown and not on the search input, so close it
        wrapper.classList.remove("active");
    }
});

optionsList.addEventListener("click", event => {
    event.stopPropagation();
    const clickedOption = event.target;
    if (clickedOption.tagName === "SPAN" || clickedOption.tagName === "LI") {
        const selectedMovie = clickedOption.textContent;
        selectMovie(selectedMovie);
    }
});


const closeButton = document.getElementById('closeBtn');
const alertDiv = document.getElementById('error')

closeButton.addEventListener('click', () => {
    // Find the parent alert div and hide it when the close button is clicked
alertDiv.style.display = 'none';
});



// Handling the form submission
const submitBtn = document.getElementById("submitBtn");
submitBtn.addEventListener("click", () => {
    // Your post request logic here
    const selectedMovie = selectedMovieInput.value;
    // Do something with the selectedMovie, like sending it in a post request
});



