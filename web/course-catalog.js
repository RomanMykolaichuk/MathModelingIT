"use strict";

globalThis.MathModelingCatalog = [
  {
    id:"t1_l1", code:"T1.L1", topic:1,
    title:"Форма і принципи представлення математичних моделей",
    status:"interactive", anchor:"#resource",
    theoryUrl:"https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l1/README.md",
    instructionPdf:"instructions/t1_l1_lab_instruction.pdf",
    challenge:"Коли математично правильна формула дає беззмістовний результат?",
    transfer:"Виділіть змінні, параметри, припущення та межі власної дослідницької моделі."
  },
  {
    id:"t1_l2", code:"T1.L2", topic:1,
    title:"Класифікація математичних моделей",
    status:"python",
    challenge:"Чи достатньо однієї детермінованої траєкторії, якщо параметри випадкові?",
    transfer:"Порівняйте детерміновану і стохастичну версії однієї задачі."
  },
  {
    id:"t1_l3", code:"T1.L3", topic:1,
    title:"Організація математичного моделювання",
    status:"python",
    challenge:"Чому колега не отримав ваш результат за тим самим описом експерименту?",
    transfer:"Сформуйте мінімальний reproducibility package для власного дослідження."
  },
  {
    id:"t1_l4", code:"T1.L4", topic:1,
    title:"Класифікація методів математичного моделювання",
    status:"python",
    challenge:"Яка властивість задачі визначає вибір методу, а не звичка дослідника?",
    transfer:"Зіставте дослідницьке питання, структуру задачі, метод і спосіб перевірки."
  },
  {
    id:"t2_l1", code:"T2.L1", topic:2,
    title:"Задачі оптимізації в середовищі VS Code",
    status:"python",
    challenge:"Коли додатковий ресурс перестає змінювати оптимальне рішення?",
    transfer:"Визначте цільову функцію, обмеження та критерій незалежної перевірки."
  },
  {
    id:"t2_l2", code:"T2.L2", topic:2,
    title:"Математична модель транспортної задачі",
    status:"python",
    challenge:"Як одна заборонена ланка змінює весь оптимальний план?",
    transfer:"Виділіть вузли, потоки, обмеження балансу і сценарні відмови."
  },
  {
    id:"t2_l3", code:"T2.L3", topic:2,
    title:"Математичні моделі задач нелінійного програмування",
    status:"python",
    challenge:"Чому success=True ще не доводить, що знайдено глобальний оптимум?",
    transfer:"Заплануйте multistart або незалежну перевірку розв’язку."
  },
  {
    id:"t2_l4", code:"T2.L4", topic:2,
    title:"Математичне моделювання із застосуванням методів мережевого планування",
    status:"interactive", anchor:"#network",
    theoryUrl:"https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l4/README.md",
    instructionPdf:"instructions/t2_l4_lab_instruction.pdf",
    challenge:"Чому затримка однієї роботи змінює строк проєкту, а іншої — ні?",
    transfer:"Перетворіть етапи власного дослідження на DAG і знайдіть bottleneck."
  },
  {
    id:"t2_l5", code:"T2.L5", topic:2,
    title:"Засоби розв’язування задач множинного вибору",
    status:"interactive", anchor:"#mcda",
    theoryUrl:"https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l5/README.md",
    instructionPdf:"instructions/t2_l5_lab_instruction.pdf",
    challenge:"Наскільки лідер залежить від ваг і способу агрегування?",
    transfer:"Перевірте, чи є ваш висновок стійким до зміни ваг і методу."
  },
  {
    id:"t2_l6", code:"T2.L6", topic:2,
    title:"Системи комп'ютерної математики та їх можливості для математичного моделювання",
    status:"python",
    challenge:"Що саме доводить збіг символічного та чисельного розв’язків?",
    transfer:"Заплануйте independent verification різними математичними представленнями."
  },
  {
    id:"t2_l7", code:"T2.L7", topic:2,
    title:"Використання систем комп’ютерної математики в наукових дослідженнях",
    status:"python",
    challenge:"Чи може мала похибка підгонки приховувати неправильну структуру моделі?",
    transfer:"Пов’яжіть калібрування, uncertainty, verification і допустимий науковий висновок."
  }
];
