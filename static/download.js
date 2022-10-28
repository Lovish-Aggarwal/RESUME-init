function generatePDF(){

    var opt = {
        margin:       1,
        filename:     'myfile.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, scrollY: 0},
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
        pagebreak: { mode: 'avoid-all'}
      };

    const pdf=document.getElementById('resume');
    html2pdf()
    .set(opt)
    .from(pdf)
    .save();
}