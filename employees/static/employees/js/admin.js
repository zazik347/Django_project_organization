(function() {
    'use strict';

    function ready() {
        if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
            (function($) {
                // Скрываем поле "Employee" — оно не нужно
                $('#id_employee').parent().parent().hide();

                // Скрываем кнопку "Save" и весь блок действий
                $('.submit-row').hide();

                $('#id_project').on('change', function() {
                    var projectId = $(this).val();
                    if (!projectId) return;

                    $.get('/get-project-dates/', { project_id: projectId }, function(data) {
                        // Подставляем даты
                        $('#id_start_date').val(data.start_date);
                        $('#id_end_date').val(data.end_date);

                        // Сохраняем данные для кнопки
                        window.projectData = data;

                        // Добавляем кнопку, если есть сотрудники
                        if (data.employees && data.employees.length > 0) {
                            if ($('#add-all-btn').length === 0) {
                                $('#id_project').parent().parent().after(`
                                    <div class="form-row">
                                        <div class="fieldBox">
                                            <input type="button" id="add-all-btn" 
                                                   value="✅ Создать для ${data.employees.length} сотрудников" 
                                                   class="default" />
                                        </div>
                                    </div>
                                `);
                            }
                        }
                    });
                });

                // Обработчик кнопки
                $(document).on('click', '#add-all-btn', function() {
                    if (!window.projectData) return;

                    if (confirm('Добавить ' + window.projectData.employees.length + ' сотрудников?')) {
                        window.projectData.employees.forEach(function(emp) {
                            fetch('/bulk-create-assignments/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                },
                                body: 'project_id=' + $('#id_project').val() +
                                      '&employee_id=' + emp.id +
                                      '&start_date=' + window.projectData.start_date +
                                      '&end_date=' + window.projectData.end_date
                            })
                            .then(r => r.text())
                            .then(text => {
                                try {
                                    const data = JSON.parse(text);
                                    if (data.status === 'success') {
                                        console.log('✅ Создано:', emp.full_name);
                                    }
                                } catch (e) {
                                    console.error('❌ Не JSON:', text);
                                }
                            })
                            .catch(err => console.error('❌ Ошибка:', err));
                        });

                        alert('✅ Все записи добавлены! Проверь список Employee Assignments');
                    }
                });
            })(django.jQuery);
        } else {
            setTimeout(ready, 100);
        }
    }

    ready();
})();
