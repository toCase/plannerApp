// const btn_add = document.querySelector('.columnB .btn-add');
// const btn_close = document.querySelector('dialog .btn-close');

// const dialog = document.querySelector('dialog');

// if (dialog.classList.contains("open")){
//     console.log("---OPEN----");
//     dialog.classList.remove("open");
//     dialog.showModal();
// }

// btn_add.addEventListener('click', () => {
//     dialog.showModal();
// })

// btn_close.addEventListener('click', () => {
//     dialog.close();
// })

// ----------------spec form
const btn_new = document.querySelector('.columnB .btn-new');
const win_form = document.querySelector('.columnB .window');
const btn_cls = document.querySelector('.columnB .window .btn-cls');


btn_new.addEventListener('click', () => {
    console.log("click open");
    win_form.classList.add("open");
})

btn_cls.addEventListener('click', () => {
    closeForm();
})


function closeForm(){
    win_form.classList.remove('open');
}

//--------------------spec table
const tab_rows = document.querySelectorAll('.columnB .spec-table tr');

tab_rows.forEach(row  => {
    row.addEventListener('click', () => {
        const act = document.querySelector('.columnB .spec-table tr.active');
        if (act != null) {
            act.classList.remove('active');
        }
        row.classList.add('active');
        closeForm();

        window.location.href('')
    })
});

