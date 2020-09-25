class Base_Index extends Grid {
    constructor() {
        super();
        Base_Index.indexes.push(this);
        this.on_edit = this.on_add;
    }

    static read() {
        Base_Index.indexes.forEach((index) => index.read());
    }

    get columns() {
        return [{
            field: 'id',
            text: 'Id',
            size: '100px',
            sortable: true,
            resizable: true,
            info: true
        }];
    }

    get columns_groups() {
        return [{
            caption: '',
            master: true 
        }];
    }

    get searches() {
        return [{
            type: 'text',
            field: 'id',
            label: 'Id'
        }];
    }
    
    highlight(id) {
        let g = this.grid;
        g.records.find((r) => r.id == id).w2ui = {
            "style": "background-color: #C2F5B4"
        };
        setTimeout(function() {
            delete g.records.find((r) => r.id == id).w2ui["style"];
            g.refresh();
        }, 3000);
    }

    on_add(event) {
        let obj = this;
        let id = this.name + '_' + event.type;
        if (!w2ui[id]) {
            $().w2form({
                name: id,
                fields: [{
                    field: 'id',
                    type: 'text',
                    required: true,
                    html: {
                        label: 'Id',
                        attr: event.type === 'edit' ? 'readonly' : ''
                    }
                }].concat(this.fields),
                record: event.type === 'edit' ? obj.grid.records[event.recid - 1] : null,
                actions: {
                    Cancel: function() {
                        w2popup.close();
                    },
                    Reset: function() {
                        if (event.type === 'edit') {
                            this.record = obj.grid.records[event.recid - 1];
                            this.refresh();
                        } else {
                            this.clear();
                        }
                    },
                    Save: function() {
                        let error = this.validate();
                        let form = this;
                        if (error.length === 0) {
                            switch (event.type) {
                                case 'add':
                                    obj.create([this.record],
                                        function(response) {
                                            obj.grid.add({... {
                                                    recid: obj.grid.records.length + 1,
                                                },
                                                ...form.record
                                            });
                                        });
                                    break;
                                case 'edit':
                                    obj.update([this.record],
                                        function(response) {
                                            obj.grid.records[event.recid - 1] = form.record;
                                            obj.grid.refresh();
                                        });
                                    break;
                            }
                            w2popup.close();
                        }
                    }
                }
            });
        } else {
            w2ui[id].clear();
        }
        $().w2popup('open', {
            title: (event.type === 'add' ? 'Add a new ' : 'Edit ') + this.label,
            body: '<div id="form" style="width: 100%; height: 100%;"></div>',
            style: 'padding: 15px 0px 0px 0px',
            width: 500,
            height: 300,
            showMax: true,
            onToggle: function(event) {
                $(w2ui[id].box).hide();
                event.onComplete = function() {
                    $(w2ui[id].box).show();
                    w2ui[id].resize();
                }
            },
            onOpen: function(event) {
                event.onComplete = function() {
                    $('#w2ui-popup #form').w2render(id);
                }
            }
        });
    }

    on_delete(event) {
        if (event.force == true) {
            this.delete(this.getSelectedRecords());
        }
    }

    on_save(event) {
        if (event.phase == 'after') {
            this.update(this.getSelectedRecords());
        }
    }

    read() {
        let obj = this;
        $.ajax({
            url: this.route,
            type: 'GET',
            success: function(response) {
                response.forEach((record) => {
                    obj.grid.add({... {
                            recid: obj.grid.records.length + 1,
                            id: record.id,
                        },
                        ...obj.read_record(record)
                    });
                })
            },
            error: (response) => log.error(response.responseJSON)
        });
    }

    create(records, success_callback, error_callback) {
        let data = records.map((r) => ({
            ... { id: r.id },
            ...this.create_record(r)
        }));
        this.__request('POST', data, success_callback, error_callback);
    }

    update(records, success_callback, error_callback) {
        let data = records.map((r) => ({
            ... { id: r.id },
            ...this.update_record(r)
        }));
        this.__request('PUT', data, success_callback, error_callback);
    }

    delete(records, success_callback, error_callback) {
        let data = { where: { or: [] } }
        records.forEach(function(r) {
            data.where.or.push({
                equals: {
                    target: 'id',
                    expr: r.id
                }
            });
        });
        this.__request('DELETE', data, success_callback, error_callback);
    }

    render(caller, record, index, column_index) {
        let id = caller.grid.getCellValue(index, column_index);
        let link = $('<span>', {
            class: 'w2ui-info w2ui-icon-info',
            onclick: `event.stopPropagation();
                        ${this.name}.highlight('${id}');
                        w2ui.sidebar.select('${this.name}');
                        w2ui.layout.html('main', w2ui['${this.name}']);`
        });
        return link.prop('outerHTML') + ' ' + id;
    }

    __request(method, data, success_callback, error_callback) {
        $.ajax({
            url: this.route,
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(data),
            dataType: 'json',
            success: (response) => {
                if (success_callback) {
                    success_callback(response.responseJSON);
                } else {
                    log.info(response.responseJSON);
                }
            },
            error: (response) => {
                if (error_callback) {
                    error_callback(response.responseJSON);
                } else {
                    log.error(response.responseJSON);
                }
            }
        });
    }

    on_expand(event) {
        $('#' + event.box_id).append(
            $('<div>')
                .append('Expanded content')
                .css('padding', '10px')
                .css('height', '100px')
        );
    }
}

Base_Index.indexes = [];
