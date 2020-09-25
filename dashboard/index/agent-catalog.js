class Agent_Catalog_Index extends Base_Index {
    constructor() {
        super();
        this.label = 'Agent Catalog';
        this.name = 'agent_catalog';
        this.route = '/catalog/agent';
        this.update_record = this.create_record;
    }

    get columns() {
        let obj = this;
        return super.columns.concat([]);
    }

    get fields() {
        return [];
    }

    get searches() {
        return super.searches.concat([]);
    }

    read_record(record) {
        return {};
    }

    create_record(record) {
        return {};
    }
}
