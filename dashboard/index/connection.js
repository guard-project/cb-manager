class Connection_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Connection';
        this.name = 'connection';
        this.route = '/connection';
        this.update_record = this.create_record;
    }

    get columns() {
        let obj = this;
        return super.columns.concat([{
            field: 'exec_env',
            text: 'Exec. Env.',
            size: '40%',
            sortable: true,
            resizable: true,
            editable: {
                type: 'list',
                items: () => w2ui.exec_env.records,
                showAll: true
            },
            render: (record, index, column_index) => exec_env.render(obj, record, index, column_index)
        }, {
            field: 'network_link',
            text: 'Network Link',
            size: '40%',
            sortable: true,
            resizable: true,
            editable: {
                type: 'list',
                items: () => w2ui.network_link.records,
                showAll: true
            },
            render: (record, index, column_index) => network_link.render(obj, record, index, column_index)
        }]);
    }

    get fields() {
        return [{
            field: 'exec_env',
            type: 'list',
            required: true,
            options: { items: () => w2ui.exec_env.records },
            html: { label: 'Exec. Env' }
        }, {
            field: 'network_link',
            type: 'list',
            required: true,
            options: { items: () => w2ui.network_link.records },
            html: { label: 'Network Link' }
        }];
    }

    get searches() {
        return super.searches.concat([{
            type: 'list',
            field: 'exec_env',
            label: 'Exec. Env.',
            items: w2ui.exec_env.records
        }, {
            type: 'list',
            field: 'network_link',
            label: 'Network Link',
            items: w2ui.network_link.records
        }]);
    }

    read_record(record) {
        return {
            exec_env: record.exec_env_id,
            network_link: record.network_link_id
        };
    }

    create_record(record) {
        return {
            exec_env_id: record.exec_env.id,
            network_link_id: record.network_link.id
        }
    }
}
