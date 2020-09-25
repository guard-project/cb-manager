class Log extends Grid {
    constructor() {
        super();
        this.label = 'Log';
        this.name = 'log';
    }

    get columns() {
        return [{
            field: 'code',
            text: 'Code',
            size: '100%',
            sortable: true,
            resizable: true
        }, {
            field: 'error',
            text: 'Error',
            size: '100%',
            sortable: true,
            resizable: true
        }, {
            field: 'message',
            text: 'Message',
            size: '100%',
            sortable: true,
            resizable: true
        }, {
            field: 'status',
            text: 'Status',
            size: '100%',
            sortable: true,
            resizable: true
        }]
    }

    get searches() {
        return [{
            type: 'int',
            field: 'code',
            label: 'Code'
        },
        {
            type: 'enum',
            field: 'error',
            label: 'Error'
        },
        {
            type: 'text',
            field: 'message',
            label: 'Message'
        },
        {
            type: 'text',
            field: 'status',
            label: 'Status'
        }];
    }

    error(record) {
        this.grid.add({...{
                recid: this.grid.records.length + 1,
                w2ui: { 
                    style: 'background-color: rgb(255, 199, 255)'
                }
            },...record
        });
    }

    info(record) {
        this.grid.add({...{
                recid: this.grid.records.length + 1,
                w2ui: { 
                    style: 'background-color: rgb(255, 255, 204)'
                }
            },...record
        });
    }
}
