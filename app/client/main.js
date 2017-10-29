import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Tasks } from '../imports/api/tasks.js';

import './main.html';

Template.hello.onCreated(function helloOnCreated() {
  // counter starts at 0
  this.counter = new ReactiveVar(0);
  this.cur_rec = new ReactiveVar('');
});

Template.hello.helpers({
  counter() {
    return Template.instance().counter.get();
  },
  all_images() {
      return Tasks.find({});
  },
  new_images() {
      return Tasks.find({is_processed: true, is_verified: false});
  },
  new_images() {
      return Tasks.find({is_processed: true, is_verified: false});
  },
  cur_image() {
      cur = Tasks.findOne({_id:Template.instance().cur_rec.get()});
      cur.is_photoshopped_confidence = parseInt(cur.is_photoshopped_confidence);
      return cur;
  },
});

Template.hello.events({
  'click .view-info'(event, instance) {
        console.log(this._id);
        instance.cur_rec.set(this._id);

    //instance.counter.set(instance.counter.get() + 1);
    /*
    Tasks.insert({
        text: 'hello: ' + instance.counter.get() ,
        createdAt: new Date(), // current time
    });
    */
  },
  'click .submit-changes'(event, instance) {
        console.log(this._id);

        Tasks.update({ _id: this._id }, {
            $set: {
                'is_verified': true,
                'is_rejected': false,
                'auto_is_correct': false,
                'manual': {
                    'name': this.auto_vals.name.value,
                    'pan': this.auto_vals.pan.value,
                    'dob': this.auto_vals.dob.value,
                    'father_name': this.auto_vals.father_name.value
                }
            }
        });
  },
  'click .info-is-correct'(event, instance) {
        console.log(this._id);

        Tasks.update({ _id: this._id }, {
            $set: {
                'is_verified': true,
                'is_rejected': false,
                'auto_is_correct': true,
            }
        });
  },
  'click .reject-record'(event, instance) {
        console.log(this._id);

        Tasks.update({ _id: this._id }, {
            $set: {
                'is_verified': true,
                'is_rejected': true,
                'auto_is_correct': true,
            }
        });
  },
});

