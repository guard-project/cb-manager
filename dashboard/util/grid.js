class Grid {
    constructor() {
        this.on_edit = this.on_add;
        this.icon = 'icon-page';

        this.label = null;
        this.name = null;
        this.route = null;
    }
    
    sidebar(selected) {
        return {
            id: this.name,
            text: this.label,
            img: this.icon,
            selected: selected
        }
    }

    get grid() {
        return w2ui[this.name];
    }

    get config() {
        return {
            name: this.name,
            show: {
                lineNumbers: true,
                expandColumn: this.on_expand !== undefined,
                selectColumn: true,
                toolbar: true,
                toolbarAdd: this.on_add !== undefined,
                toolbarDelete: this.on_delete !== undefined,
                toolbarSave: this.on_save !== undefined,
                toolbarEdit: this.on_edit !== undefined,
                footer: true
            },
            reorderRows: true,
            multiSearch: true,
            columnGroups: this.column_groups,
            columns: this.columns,
            menu: ['TODO'],
            records: [],
            searches: [{
                type: 'int',
                field: 'recid',
                label: '#'
            }].concat(this.searches),
            onExpand: (event) => this.on_expand && this.on_expand(event),
            onAdd: (event) => this.on_add && this.on_add(event),
            onEdit: (event) => this.on_edit && this.on_edit(event),
            onDelete: (event) => this.on_delete && this.on_delete(event),
            onSave: (event) => this.on_save && this.on_save(event)
        }
    }

    getSelectedRecords() {
        let rec_ids = this.grid.getSelection();
        return rec_ids.map((rec_id) => this.grid.records[rec_id - 1]);
    }
}
