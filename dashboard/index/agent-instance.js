class Agent_Instance_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Agent Instance';
        this.name = 'agent_instance';
        this.route = '/instance/agent';
        this.update_record = this.create_record;
    }

    get columns() {
        let obj = this;
        return super.columns.concat([{
            field: 'catalog',
            text: 'Catalog',
            size: '40%',
            sortable: true,
            resizable: true,
            editable: {
                type: 'list',
                items: () => w2ui.agent_catalog.records,
                showAll: true
            },
            render: (record, index, column_index) => agent_catalog.render(obj, record, index, column_index)
        }, {
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
        }]);
    }

    get fields() {
        return [{
            field: 'catalog',
            type: 'list',
            required: true,
            options: { items: () => w2ui.agent_catalog.records },
            html: { label: 'Catalog' }
        }, {
            field: 'exec_env',
            type: 'list',
            required: true,
            options: { items: () => w2ui.exec_env.records },
            html: { label: 'Exec. Env' }
        }];
    }

    get searches() {
        return super.searches.concat([{
            type: 'list',
            field: 'catalog',
            label: 'Catalog',
            items: w2ui.agent_catalog.records
        }, {
            type: 'list',
            field: 'exec_env',
            label: 'Exec. Env.',
            items: w2ui.exec_env.records
        }]);
    }

    read_record(record) {
        return {
            catalog: record.agent_catalog_id,
            exec_env: record.exec_env_id
        };
    }

    create_record(record) {
        return {
            agent_catalog_id: record.catalog.id,
            exec_env_id: record.exec_env.id
        }
    }
}
