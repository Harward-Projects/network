// document.addEventListener('DOMContentLoaded', function () {
//   // Use links to toggle between views
// });

// Function: Create the button element
const buttonCreator = function (buttonName, postId) {
  const button = document.createElement('button');
  button.id = `${buttonName}ButtonPost_${postId}`;
  // Capitalize the buttonName
  const buttonNameCapitalized =
    buttonName.charAt(0).toUpperCase() + buttonName.slice(1);
  button.textContent = buttonNameCapitalized;
  button.className = 'card-link';
  return button;
};

// Function: Create the textContainer element, either 'p' or 'textarea'
const textContainerCreator = function (type, content, postId) {
  const textContainer = document.createElement(type);
  if (type == 'p') {
    textContainer.textContent = content; // Use textContent for paragraphs
    textContainer.id = `postContentParagraph_${postId}`;
    textContainer.className = 'mt-2 mb-2';
  } else {
    textContainer.id = `postContentTextarea_${postId}`;
    textContainer.className = 'form-control mb-1';
    textContainer.rows = 3;
    textContainer.textContent = content; // Set value property for textarea
  }
  return textContainer;
};

// Function: Substitute the old element by new element
const elementSubstitutor = function (oldElement, newElement) {
  oldElement.parentNode.replaceChild(newElement, oldElement);
};

// Function: Update the post content in the database
const postUpdaterInDataBase = function (newPostContent, postId) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch(`/post/${postId}/edit/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      new_post_content: newPostContent,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to update the post.');
      }
      // Handle successful response...
    })
    .catch((error) => {
      console.error('Error updating the post:', error);
    });
};

// Function: Performs editButton Actions
const editButtonActions = function (event, postId) {
  const editButton = event.target;
  // Create saveButton element
  const saveButton = buttonCreator('save', postId);
  // Replace old editButton with the new saveButton
  editButton.parentNode.replaceChild(saveButton, editButton);
  // Create cancelButton element
  const cancelButton = buttonCreator('cancel', postId);
  // Append the cancelButton to the saveButton
  saveButton.parentNode.append(cancelButton);
  // Get the paragraph element
  const paragraph = document.getElementById(`postContentParagraph_${postId}`);
  // Keep the textContent of the paragraph for cancel click if any
  paragraphContent = paragraph.textContent;
  // Create the textarea element
  const textarea = textContainerCreator(
    'textarea',
    paragraph.textContent,
    postId
  );
  // Replace old paragrap with the new textarea
  paragraph.parentNode.replaceChild(textarea, paragraph);
};

// Function: Performs saveButton Actions
const saveButtonActions = function (event, postId) {
  const saveButton = event.target;
  // Create editButton element
  const editButton = buttonCreator('edit', postId);
  // Replace old saveButton with the new editButton
  saveButton.parentNode.replaceChild(editButton, saveButton);
  // Remove cancelButton element
  const cancelButton = document.getElementById(`cancelButtonPost_${postId}`);
  cancelButton.remove();
  // Get the textarea element
  const textarea = document.getElementById(`postContentTextarea_${postId}`);
  // Create the paragraph element
  const paragraph = textContainerCreator('p', textarea.value, postId);
  // Update the post content in the database
  postUpdaterInDataBase(textarea.value, postId);
  // Replace old textarea with the new paragraph
  textarea.parentNode.replaceChild(paragraph, textarea);
};

// Function: Performs saveButton Actions
const cancelButtonActions = function (event, postId) {
  const cancelButton = event.target;
  // Create editButton element
  const editButton = buttonCreator('edit', postId);
  // Replace old saveButton with the new editButton
  const saveButton = document.getElementById(`saveButtonPost_${postId}`);
  saveButton.parentNode.replaceChild(editButton, saveButton);
  // Remove cancelButton element
  cancelButton.remove();
  // Get the textarea element
  const textarea = document.getElementById(`postContentTextarea_${postId}`);
  // Create the paragraph element
  const paragraph = textContainerCreator('p', paragraphContent, postId);
  // Replace old textarea with the new paragraph
  textarea.parentNode.replaceChild(paragraph, textarea);
};

let paragraphContent,
  postUnderEditId = false;
// This section grabs visible editButtonPost_id's buttons and performs edit by means of fetch method (POST) and Django edit_post function
// The url get path for edit_post function must be considered for security and/or clean code to be unreachable
document.addEventListener('click', (event) => {
  let eventId, postId;
  eventId = event.target.id;
  postId = eventId.split('_')[1]; // Split the id string and get the second part (post.id)
  // If editButton clicked
  if (event.target.id.startsWith('editButtonPost_')) {
    if (postUnderEditId == false) {
      editButtonActions(event, postId);
      postUnderEditId = true;
    } else {
      alert('First assign the POST UNDER EDIT!');
    }
  }

  // If saveButton clicked
  // Performs front and back manipulation by means of fetch method (POST) and Django edit_post function
  if (event.target.id.startsWith('saveButtonPost_')) {
    saveButtonActions(event, postId);
    postUnderEditId = false;
  }

  // If cancelButton clicked
  if (event.target.id.startsWith('cancelButtonPost_')) {
    cancelButtonActions(event, postId);
    postUnderEditId = false;
  }

  //If like/unlike span clicked
  // Performs front and back manipulation by means of fetch method (PUT) and Django like_unlike_post function
  if (event.target.id.startsWith('likeIconForPost_')) {
    if (postUnderEditId == true) {
      alert('First assign the POST UNDER EDIT!');
    } else {
      const likeIcon = event.target;
      // This if statement is to tackle authentication recognition status from the new post.
      if (document.getElementById('newPostId')) {
        console.log('User is logged in');
        if (likeIcon.style.color != 'red') {
          likeIcon.style.color = 'red';
        } else {
          likeIcon.style.color = '#818a91';
        }

        const likeCountId = `likeCountForPost_${postId}`;
        const likeCountElement = document.getElementById(likeCountId);
        const csrfName = '[name=csrfmiddlewaretoken]';
        const csrftoken = document.querySelector(csrfName).value;
        fetch(`/post/${postId}/like/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({
            liked: likeIcon.style.color === 'red', // Determine liked based on the color
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Failed to update post like/unlike state.');
            }
            return response.json();
          })
          .then((data) => {
            likeCountElement.textContent = data.like_count;
          })
          .catch((error) => {
            console.error('Error updating post like/unlike state:', error);
          });
      } else {
        alert('Please log in to perform this action.');
      }
    }
  }
});
