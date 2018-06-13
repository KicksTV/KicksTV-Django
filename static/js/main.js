// Global Variables

var greyOverlay = document.getElementById("grey-overlay");
var detailImageContainer = document.getElementById("detailImageContainer");
var imgContainer = document.getElementById("imgContainer");
var imgContainerTitle = document.getElementById("imgContainerTitle");




// Code for creating enlarged view of image from gallery
function viewImage(con, image_title) {	
	var allText = image_title;
	var imgOriSize = getImgSize(con.children[0].src);
	var windowSize = alertSize();
	var newImgHeight = windowSize[1] - 200;

	windowSize[1] -= 132;

	if (imgOriSize.height > imgOriSize.width) {
		if (imgOriSize.height > windowSize[1]) {
			imgContainer.style.height = newImgHeight.toString() + "px";
		}
	}

	imgContainer.src = con.childNodes[1].src;
	imgContainerTitle.innerHTML = allText;
	greyOverlay.style.display = "block";
	detailImageContainer.style.display = "block";
}

// Closes that view
function closeImage() {
	greyOverlay.style.display = "none";
	detailImageContainer.style.display = "none";
	imgContainer.style.height = "auto";
}

// Code for getting original dimentions of an image
function getImgSize(imgSrc) {
	var newImg = new Image();
	newImg.src = imgSrc;
	return newImg;
}

// Code for adding classes to form elements
window.onload = function addClass() {
	var inputs = document.getElementsByTagName("input");
	var labels = document.getElementsByTagName("label");

	for (var i=0;i<inputs.length;i++) {
		if (inputs[i].id.indexOf("id_") !== -1) {
			if (inputs[i].type == "text") {
				inputs[i].classList.add("form-control");
			}
		}
	}
	for (var i=0;i<labels.length;i++) {
		if (labels[i].classList.item(0) !== null) {
			if (labels[i].classList.item(0).indexOf("control-label")) {
				return;
			}
		}else{
			if (labels[i].id.indexOf("id")) {
				if (labels[i].innerHTML !== "Gallery image:" && labels[i].innerHTML !== "Image image:" && labels[i].innerHTML !== "Image:") {
					labels[i].classList.add("input-group-addon");
				}
			}
		}
	}
}

function confirmDelete(title) {
	var container = document.getElementById("confirmDeleteContainer");
	var containerTitle = document.getElementById("confirmDeleteTitle");
	var whiteContainer = document.getElementById("whiteContainer");


	whiteContainer.style.display = "block";
	whiteContainer.style.zIndex = "5000";

	containerTitle.innerHTML = title;
	container.style.display = "block";
}

function cancelDelete() {
	var container = document.getElementById("confirmDeleteContainer");
	var whiteContainer = document.getElementById("whiteContainer");

	container.style.display = "none";
	whiteContainer.style.display = "none";
}

function alertSize() {
	var myWidth = 0, myHeight = 0;
	
	if( typeof( window.innerWidth ) == 'number' ) {
		//Non-IE
		myWidth = window.innerWidth;
		myHeight = window.innerHeight;
	} else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
		//IE 6+ in 'standards compliant mode'
		myWidth = document.documentElement.clientWidth;
		myHeight = document.documentElement.clientHeight;
	} else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
		//IE 4 compatible
		myWidth = document.body.clientWidth;
		myHeight = document.body.clientHeight;
	}
	return [myWidth, myHeight];
}