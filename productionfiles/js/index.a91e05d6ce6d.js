console.log('sanity check')

let alertBox = document.querySelector('.alert_box');
let alertCloseBtn = document.querySelector('#alert-close-btn')
let navBar = document.querySelector('.navigation')
let navToggleBtn = document.querySelector('.nav_toogle_btn')
let hamburger = document.querySelector('#hamburger')
let crossSign = document.querySelector('#cross_sign')
let navSearchBtn = document.querySelector('#nav_search_btn')
let navSearchBar = document.querySelector('.nav_search_bar')
let commentButtonDiv = document.querySelector('.comment_button_div');
let commentStaticsSmall = document.querySelector('.comment_static_small');
let commentSection = document.querySelector('.post_comment_section');
let replyBoxBtn = document.querySelector('.reply_box_btn');
let inputForReply = document.querySelector('.input_for_reply');

const button_nodelist = document.querySelectorAll('.comment_button_div');
const staticSmall_nodelist = document.querySelectorAll('.comment_static_small');
const reply_box_list = document.querySelectorAll('.reply_box_btn');
const comment_buttons = Array.from(button_nodelist);
const staticSmall_list = Array.from(staticSmall_nodelist);
const replyBox_list = Array.from(reply_box_list);
const carousel = document.querySelector('.carousel');
const slides = document.querySelectorAll('.carousel-slide');



// alert close btn
if (alertBox){
  console.log(alertBox)
  alertCloseBtn.addEventListener('click', ()=>{
    alertBox.style.display = 'none'
  })
}

// nav close btn

navToggleBtn.addEventListener('click', function() {
  console.log('clicked');

  // Check the current display style of the navigation menu
  const navBarStyle = getComputedStyle(navBar);

  if (navBarStyle.display === 'flex') {
    // If the navigation menu is currently displayed, hide it
    navBar.style.display = 'none';
    console.log('navbar is now hidden');
  
    // Show the hamburger icon and hide the cross icon
    hamburger.style.display = 'block';
    crossSign.style.display = 'none';
  } else {
    // If the navigation menu is currently hidden, display it
    navBar.style.display = 'flex';
    console.log('navbar is now displayed');
  
    // Show the cross icon and hide the hamburger icon
    crossSign.style.display = 'block';
    hamburger.style.display = 'none';
  }
});

// nav search btn
navSearchBtn.addEventListener('click', function(){
  console.log('clicked')
  let navSearchbarstyle = getComputedStyle(navSearchBar)

  if (navSearchbarstyle.display === 'none'){
    navSearchBar.style.display = 'block'
    console.log('changed to block')
  }else{
    navSearchBar.style.display = 'none'
    console.log('changed to none')
  }
})

//function to remove nav item search in screen wider than 1024
function removeNavSearchOnlargeScreen(){
  const screenwidth = window.innerWidth
  console.log(screenwidth)
  if (screenwidth > 1024){
    const navUl = document.querySelector('.nav_ul')
    const removeSearchBtn = navUl.querySelector('.search_btn_holder')
    // const lastChild = navSearchBar
    
    console.log(removeSearchBtn)

    if (removeSearchBtn){
      navUl.removeChild(removeSearchBtn)
      console.log('removed last child')
    }

  }
}
removeNavSearchOnlargeScreen();
window.addEventListener('resize', removeNavSearchOnlargeScreen);

// JavaScript to handle carousel functionality
// if pore add korsi, js crask na korar jonno

let currentIndex = 0;

if (carousel){

  function showSlide(index) {
    carousel.style.transform = `translateX(-${index * 100}%)`;
  }
  
  function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
  }
  
  function prevSlide() {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
  }
  
  // Add event listeners for next and previous buttons
  if (document.querySelector('#next')){
    document.querySelector('#next').addEventListener('click', nextSlide);
    document.querySelector('#prev').addEventListener('click', prevSlide);
  }
  
  // Show the first slide
  showSlide(currentIndex);
}




// comment button opens comment section 
comment_buttons.forEach(function(button){
  let buttons_top_level_parent = button.parentElement.parentElement
  let comment_section = buttons_top_level_parent.lastElementChild

  button.addEventListener('click', ()=>{
    comment_section.classList.toggle('display_block');
  })
  console.log('Comment_btn working')
})

// comments small tag opens comment section 
staticSmall_list.forEach(function(small){
  let smalls_top_level_parent = small.parentElement.parentElement
  let comment_section = smalls_top_level_parent.lastElementChild

  small.addEventListener('click', ()=>{
    comment_section.classList.toggle('display_block');
  })
  console.log('smalls btn working')
})

// reply small opens reply input 
replyBox_list.forEach(function(small){
  let reply_smalls_top_level_parent = small.parentElement.parentElement
  let input_for_reply = reply_smalls_top_level_parent.lastElementChild

  small.addEventListener('click', ()=>{
    input_for_reply.classList.toggle('display_block')
  })
  console.log('reply_btn working')
})
