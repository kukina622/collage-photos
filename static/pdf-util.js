const Base64Prefix = "data:application/pdf;base64,";
let pdf = null;
let currentPageNo = 1;

function getPdfHandler() {
  return window["pdfjs-dist/build/pdf"];
}

function readBlob(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => resolve(reader.result));
    reader.addEventListener("error", reject);
    reader.readAsDataURL(blob);
  });
}

async function readPDFFile(pdfData) {
  pdfData = pdfData instanceof Blob ? await readBlob(pdfData) : pdfData;
  const data = atob(
    pdfData.startsWith(Base64Prefix)
      ? pdfData.substring(Base64Prefix.length)
      : pdfData
  );

  return pdfjsLib.getDocument({ data: data }).promise;
}

async function renderPage(pageNo) {
  const page = await pdf.getPage(pageNo);

  console.log("Page loaded");

  var scale = 1.5;
  var viewport = page.getViewport({ scale: scale });

  // Prepare canvas using PDF page dimensions
  var canvas = document.getElementById("pdf-render-canvas");
  var context = canvas.getContext("2d");
  canvas.height = viewport.height;
  canvas.width = viewport.width;

  // Render PDF page into canvas context
  var renderContext = {
    canvasContext: context,
    viewport: viewport
  };
  var renderTask = page.render(renderContext);
  await renderTask.promise;
}

function pdfChangePage(type = "next") {
  switch (type) {
    case "next":
      if (currentPageNo >= pdf.numPages) {
        return;
      }
      currentPageNo++;
      break;
    case "prev":
      if (currentPageNo <= 1) {
        return;
      }
      currentPageNo--;
      break;
  }
  renderPage(currentPageNo);
  document.getElementById("current-page-no").innerText = `第${currentPageNo}頁`;
}

async function initPdf(url) {
  pdf = await pdfjsLib.getDocument(url).promise;
  console.log(pdf);
  renderPage(1);
}

document
  .getElementById("pdf-prev")
  ?.addEventListener("click", () => pdfChangePage("prev"));

document
  .querySelector("#pdf-next")
  ?.addEventListener("click", () => pdfChangePage("next"));

document.addEventListener("keydown", (e) => {
  switch (e.key) {
    case "ArrowLeft":
      pdfChangePage("prev");
      break;
    case "ArrowRight":
      pdfChangePage("next");
      break;
  }
});
