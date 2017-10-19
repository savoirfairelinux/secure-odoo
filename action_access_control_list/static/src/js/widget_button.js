odoo.define('action_access_control_list', function (require) {
"use strict";

var Model = require('web.DataModel');
var WidgetButton = require('web.form_widgets').WidgetButton;

var acl_deferred = $.Deferred();
var action_data = {};

new Model('res.users').call('get_action_access').then(function(result) {
    result.forEach(function(a){
        if(a.type === 'python'){
            action_data[a.model + ':' + a.technical_name] = a.domain;
        }
        else if(a.type === 'action'){
            action_data[a.model + ':' + a.action_id] = a.domain;
        }
    });
    acl_deferred.resolve();
});

WidgetButton.include({
    template: 'WidgetButton',
    init: function(field_manager, node) {
        this._super(field_manager, node);
        var type = node.attrs.type
        if(type === 'object' || type === 'action'){
            var self = this;
            _.filter(field_manager.__edispatcherRegisteredEvents, function(event) {
                return event.name === "view_content_has_changed" && event.source === self;
            }).forEach(function(event){
                field_manager.__edispatcherEvents.off(event.name, event.source, event.func);
            });

            this._action = field_manager.model + ':' + node.attrs.name;
            field_manager.on("view_content_has_changed", this, function() {
                self.process_invisible_modifier();
            });
            acl_deferred.done(function(){
                self.process_invisible_modifier();
            });
        }
        else{
            this._action = null;
        }
    },
    process_invisible_modifier: function() {
        var val;
        if(this._action && this._action in action_data){
            var access = action_data[this._action];
            if(access === false){
                val = true;
            }
            else{
                if(this._ic_invisible_modifier === true){
                    val = false;
                }
                else{
                    val = this._ic_field_manager.compute_domain(this._ic_invisible_modifier);
                }
                if(access !== false){
                    val = val || !this._ic_field_manager.compute_domain(access);
                }
            }
        }
        else{
            val = this._ic_field_manager.compute_domain(this._ic_invisible_modifier);
        }
        this.set({'invisible': val});
    },
});


require('web.Sidebar').include({
    redraw: function() {
        var view = this.getParent();
        if(view.fields_view.type !== 'form'){
            return this._super(this);
        }

        var all_items = Object.assign({}, this.items);
        var self = this;
        this.items.print = all_items.print.filter(function(item){
            return self._is_item_visible(item, view);
        });
        this.items.other = all_items.other.filter(function(item){
            return self._is_item_visible(item, view);
        });

        this._super(this);
        this.items = all_items;
    },
    _is_item_visible: function(item, view){
        if(!item.action){
            return true;
        }
        var action = view.fields_view.model + ':' + item.action.id;
        if(!(action in action_data)){
            return true;
        }
        var access = action_data[action];
        if(access === true){
            return true;
        }
        else if(access === false){
            return false;
        }
        else{
            return view.compute_domain(access);
        }
    },
});

});
