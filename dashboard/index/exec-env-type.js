class Exec_Env_Type_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Exec Env Type';
        this.name = 'exec_env_type';
        this.route = '/type/exec-env';
        this.create_record = this.read_record;
        this.update_record = this.read_record;
    }

    get columns() {
        return super.columns.concat([{
            field: 'name',
            text: 'Name',
            size: '100%',
            sortable: true,
            resizable: true,
            editable: { type: 'text' }
        }]);
    }

    get fields() {
        return [{
            field: 'name',
            type: 'text',
            required: true,
            html: { label: 'Name' }
        }];
    }

    get searches() {
        return super.searches.concat([{
            type: 'text',
            field: 'name',
            label: 'name'
        }]);
    }

    read_record(record) {
        return { name: record.name };
    }
}
