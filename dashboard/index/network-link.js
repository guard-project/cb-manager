class Network_Link_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Network Link';
        this.name = 'network_link';
        this.route = '/network-link';
        this.update_record = this.create_record;
    }

    get columns() {
        let obj = this;
        return super.columns.concat([{
            field: 'type',
            text: 'Type',
            size: '40%',
            sortable: true,
            resizable: true,
            editable: {
                type: 'list',
                items: () => w2ui.network_link_type.records,
                showAll: true
            },
            render: (record, index, column_index) => network_link_type.render(obj, record, index, column_index)
        }]);
    }

    get fields() {
        return [{
            field: 'type',
            type: 'list',
            required: true,
            options: { items: () => w2ui.network_link_type.records },
            html: { label: 'Type' }
        }];
    }

    get searches() {
        return super.searches.concat([{
            type: 'list',
            field: 'type',
            label: 'Type',
            items: w2ui.network_link_type.records
        }]);
    }

    read_record(record) {
        return { type: record.type_id };
    }

    create_record(record) {
        return { type_id: record.type.id };
    }
}
