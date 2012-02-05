function addJavascript(js_path, parentTag) {
    /* Adds a <script /> tag for a given JS path.
       usefull for deferred loading of JS files. */
    var parent = document.getElementsByTagName(parentTag)[0];
    var scr = document.createElement('script');
    scr.setAttribute('type', 'text/javascript');
    scr.setAttribute('src', js_path);
    parent.appendChild(scr);
}

function addJQeventHandlerForLargeTable() {
    /* Add (1) event handler on table element.
       on click, it will find the link inside the row clicked and follow URL */
    $("table").click(function (event) {
        var target = $(event.target);
        if (target.is("td"))
            elem = target.parent()
        else 
            elem = target
        url = elem.find("a").attr('href');
        if (url)
            location.href = url;
    });
}

function addClickClassToTRElements() {
    /* adds the .click class to all TR elements with a link inside.
       this prevent filling-up HTML with useless tags on large tables */
    $("tr").each(function () {
        if ($(this).children("td").children("a").attr('href'))
            $(this).addClass('click');
    });
}

function addMessagesClickEvent() {
    $("ul#messages").click(function(event){$(this).hide("slow"); });
}

function addLogoClickEvent(base_url) {
    $("#logo").click(function(event) { location.href = base_url; });
    $(".anchor").click(function(event){ event.preventDefault();
        $('html, body').animate({scrollTop:0}, 500);
    });
}

function addJQEventsForValidationList() {
    $("#not_validated tr").click(function (event) {
        url = $(this).children("td").children("a").attr('href');
        if (url)
            location.href = url;
    });
    $("#not_validated tr").each(function () {
        if ($(this).children("td").children("a").attr('href'))
            $(this).addClass('click');
    });
}

function addJQEventCustomFileInput() {
    $("#excel-form").mouseleave(function(event) {
        value = "Parcourir…";
        if ($(this).val())
            value = $(this).val();
        $("#fakefield").prop('value', value);
    });
}

function addJQEventsSubMenu(base_url, base_url_zero, period_str, section, sub_section) {
    $("#submenu select.browser").change(function (event) {
        value = $(this).val();
        if (!value)
            return;

        if (value != "-1") {
            url = base_url_zero.replace('0', value);
        } else {
            select_id = $(this).attr('id');
            sid = parseInt(select_id.charAt(select_id.length -1));
            if (sid == 0)
                url = base_url;
            else {
                url = base_url_zero.replace('0', $("#browser_select" + (sid - 1)).val());
            }
        }
        if (section != null && value != "-1") {
            url += '/' + period_str + '/section' + section;
            if (sub_section != null) {
                url += '/' + sub_section;
            }
        }
        location.href = url;
    });
}

function addJQEventsForValidationChange(base_url) {
    $("form#report_form input, form#report_form select").change(function (event) {
        $(this).parent().addClass('changed');
    });
    $("#reset_button").click(function (event) {
        event.preventDefault();
        $("form#report_form input, form#report_form select").parent().removeClass('changed');
        $("form#report_form").get(0).reset();
    });
    $("form").submit(function (event) {});
    $("#validate_form").click(function (event) {
        event.preventDefault();
        if (confirm("Êtes vous sûr de vouloir valider le rapport ?\nUne fois validé, il ne sera plus modifiable.")) {
            location.href = base_url;
        }
    });
}

function addJQEventPeriodChange(base_url, current_entity) {
    $("#period_select").change(function (event) {
        value = $(this).val();
        url = base_url.replace('ent_code', current_entity).replace('111111', value);
        location.href = url;
    });
}

function addJQEventToggleSources() {
    $("#toggle_sources").click(function (event) {
        $("#sources").toggle("quick");
    });
}

function addJQEventPeriodsChange(base_url, current_entity, section, sub_section) {
    $("#period_nav select").change(function (event) {
        speriod = $("#speriod_select").val();
        eperiod = $("#eperiod_select").val();
        url = base_url.replace('ent_code', current_entity).replace('111111', speriod).replace('222222', eperiod);
        if (section != null) {
            url += '/section' + section;
            if (sub_section != null) {
                url += '/' + sub_section;
            }
        }
        location.href = url;
    });
}

function addJQEventForHelpNavigation() {

    $("#content").click(function (event) {
        var target = $(event.target);
        if (target.is("div"))
            elem = target
        else if (target.is("a")) {
            // special case for topic list
            if (target.parent().parent().hasClass('help')) {
                name = target.attr('href').replace('#', '');
                elem = $("#content div a[name*="+name+"]").parent();
            } else {
                // regular inside link.
                return;
            }
        } else if (target.is("li"))
            elem = target.parent().parent()
        else
            elem = target.parent()

        $("#content div").removeClass("helpon");
        elem.addClass("helpon");
    });
}

function addJQEventFormChange() {

    auto_fields = {
        "total_beginning": ['total_beginning_m', 'total_beginning_f'],
        "crit_admitted": ['hw_b7080_bmi_u18', 'muac_u120', 'hw_u70_bmi_u16',
                     'muac_u11_muac_u18', 'oedema', 'other'],
        "admitted": ['new_case', 'relapse', 'returned', 'nut_tranfered_in', 
                     'nut_referred_in'],
    }

    ages = ['u6', 'u59', 'o59', 'fu1', 'pw', 'fu12']

    function field_prefix(field) {
        for (var i in ages) {
            if (field.indexOf(ages[i] + '_') == 0) {
                return ages[i];
            }
        }
        return null;
    }

    function get_auto_field(field) {
        for (var key in auto_fields) {
            if (auto_fields[key].indexOf(field) != -1)
                return key;
        }
        return null;
    }

    function update_auto_field(report, prefix, target) {

        target_id = "auto-" + report + "-" + prefix + "_" + target;
        value = 0;
        for (var i in auto_fields[target]) {
            f_id = 'id_' + report + "-" + prefix + "_" + auto_fields[target][i];
            field = $('#' + f_id);
            // missing fields have no name prop
            if (field.prop('name') != undefined)
                value += parseInt(field.val());
        }
        if (isNaN(value))
            value = '?';
        $('#'+target_id).html(value);
    }

    function update_column_total(field) {
        column_index = null;
        ftr = field.parent().parent();
        ftd = field.parent('td');

        ftr.children('td').each(function (index) {
            if (ftd.is(ftr.children('td').get(index)))
                column_index = index;
        });

        table = field.parent().parent().parent();

        total_value = 0;
        table.children('tr').each(function (index) {
            tr = table.children('tr').get(index);
            td = $(tr).children('td').get(column_index);
            col_value = $(td).children('input').first().val();
            if (col_value != undefined) {
                total_value += parseInt(col_value);
            }
        });
        
        total_tr = table.children('tr:last-child');
        total_td = total_tr.children('td').get(column_index);

        if (isNaN(total_value))
            total_value = '?';
        $(total_td).html(total_value);
    }

    $('input').change(function () {
        // update bottom line total
        update_column_total($(this));

        from_name = $(this).prop('name');
        from_name_data = from_name.split('-');
        from_report = from_name_data[0];
        from_field = from_name_data[1];
        from_prefix = field_prefix(from_field);

        if (from_prefix != null) {
            from_field = from_field.replace(from_prefix + '_', '')
        }

        target_field = get_auto_field(from_field);

        if (target_field == null)
            return false;
        else {
            update_auto_field(from_report, from_prefix, target_field);
        }
    });
}