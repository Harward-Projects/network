// document.addEventListener('DOMContentLoaded', function () {
//   // Use links to toggle between views
// });

// const submitPostButton = document.getElementById('submitPost');

// submitPostButton.addEventListener('click', (event) => {
//   event.preventDefault(); // Prevent the default submit action

//   // Perform any custom logic here, such as validation or custom form submission
// });

const editPostButton = document.querySelectorAll('[id^="editPost_"]');
editPostButton.forEach((button) => {
  button.addEventListener('click', () => {
    const buttonId = button.id;
    console.log('Button clicked', buttonId);
  });
});

const likeIconForPost = document.querySelectorAll('[id^="likeIconForPost_"]');
likeIconForPost.forEach((likeIcon) => {
  likeIcon.addEventListener('click', () => {
    if (likeIcon.style.color != 'red') {
      likeIcon.style.color = 'red';
    } else {
      likeIcon.style.color = '#818a91';
    }
  });
});

editPostButton.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default submit action

    // Perform any custom logic here, such as validation or custom form submission
  });
});
