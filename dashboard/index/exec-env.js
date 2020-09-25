class Exec_Env_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Exec Env';
        this.name = 'exec_env';
        this.route = '/exec-env';
        this.update_record = this.create_record;
    }

    get columns() {
        let obj = this;
        return super.columns.concat([{
            field: 'hostname',
            text: 'Hostname',
            size: '180px',
            sortable: true,
            resizable: true,
            editable: { type: 'alphanumeric' }
        }, {
            field: 'type',
            text: 'Type',
            size: '40%',
            sortable: true,
            resizable: true,
            editable: {
                type: 'list',
                items: () => w2ui.exec_env_type.records,
                showAll: true
            },
            render: (record, index, column_index) => exec_env_type.render(obj, record, index, column_index)
        }, {
            field: 'lcp_started',
            text: 'Started',
            size: '120px',
            sortable: true,
            resizable: true
        }, {
            field: 'lcp_last_heartbeat',
            text: 'Last hearbeat',
            size: '120px',
            sortable: true,
            resizable: true
        }, {
            field: 'lcp_port',
            text: 'port',
            size: '120px',
            sortable: true,
            resizable: true
        }]);
    }
    
    get columns_groups() {
        return super.column_groups.concat([{
            caption: '',
            master: true
        }, {
            caption: '',
            master: true
        }, {
            caption: 'LCP',
            span: 3
        }]);
    }

    get fields() {
        return [{
            field: 'hostname',
            type: 'alphanumeric',
            required: true,
            html: { label: 'Hostname' }
        }, {
            field: 'type',
            type: 'list',
            required: true,
            options: { items: () => w2ui.exec_env_type.records },
            html: { label: 'Type' }
        }, {
            field: 'lcp_port',
            type: 'int',
            required: true,
            html: { label: 'LCP Port' }
        }];
    }

    get searches() {
        return super.searches.concat([{
            type: 'text',
            field: 'hostname',
            label: 'Hostname'
        }, {
            type: 'list',
            field: 'type',
            label: 'Type',
            items: w2ui.exec_env_type.records
        }, {
            type: 'date',
            field: 'lcp_started',
            label: 'Started'
        }, , {
            type: 'date',
            field: 'lcp_last_heartbeat',
            label: 'Last heartbeat'
        }, , {
            type: 'int',
            field: 'lcp_port',
            label: 'Port'
        }]);
    }

    read_record(record) {
        return {
            hostname: record.hostname,
            type: record.type_id,
            lcp_started: record.lcp.started,
            lcp_last_heartbeat: record.lcp.last_heartbeat,
            lcp_port: record.lcp.port
        };
    }

    create_record(record) {
        return {
            hostname: record.hostname,
            type_id: record.type.id,
            lcp: {
                port: record.lcp_port
            }
        }
    }
}
