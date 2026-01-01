const test = require('node:test');
const assert = require('assert');
const { MyClass, Student } = require('./main');

test("Test MyClass's addStudent", () => {
    const myClass = new MyClass();
    assert.strictEqual(myClass.students.length, 0);
    assert.strictEqual(myClass.addStudent(new Student()), 0);
    assert.strictEqual(myClass.addStudent("123"), -1);
});

test("Test MyClass's getStudentById", () => {
    const myClass = new MyClass();
    assert.strictEqual(myClass.getStudentById(0), null);
    const student1 = new Student();
    student1.setName("John");
    const studentId1 = myClass.addStudent(student1);
    assert.strictEqual(myClass.getStudentById(studentId1), student1);
});

test("Test Student's setName", () => {
    const student1 = new Student();
    assert.strictEqual(student1.getName(), "");
    student1.setName(123);
    assert.strictEqual(student1.getName(), "");
    student1.setName("John");
    assert.strictEqual(student1.getName(), "John");
});

test("Test Student's getName", () => {
    const student1 = new Student();
    assert.strictEqual(student1.getName(), "");
    student1.setName("John");
    assert.strictEqual(student1.getName(), "John");
});
