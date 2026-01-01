const { describe, it, beforeEach } = require('node:test');
const assert = require('assert');
const { Calculator } = require('./main');

describe('Calculator', () => {
  let calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe('exp method', () => {
    const expValidTests = [
      {
        name: 'Return 1 when input is zero',
        input: 0,
        expected: 1
      },
      {
        name: 'Return Euler number when input is 1',
        input: 1,
        expected: Math.E
      },
      {
        name: 'Return reciprocal of Euler number when input is -1',
        input: -1,
        expected: 1 / Math.E
      },
      {
        name: 'Return e squared when input is 2',
        input: 2,
        expected: Math.exp(2)
      },
      {
        name: 'Return square root of e when input is 0.5',
        input: 0.5,
        expected: Math.exp(0.5)
      }
    ];

    expValidTests.forEach(({ name, input, expected }) => {
      it(name, () => {
        const result = calculator.exp(input);
        assert.strictEqual(result, expected);
      });
    });

    const expErrorTests = [
      {
        name: 'Throw unsupported operand type error when input is NaN',
        input: NaN,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw unsupported operand type error when input is Infinity',
        input: Infinity,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw unsupported operand type error when input is negative Infinity',
        input: -Infinity,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw overflow error when input causes exponential overflow',
        input: 710,
        expectedError: 'overflow'
      }
    ];

    expErrorTests.forEach(({ name, input, expectedError }) => {
      it(name, () => {
        assert.throws(() => {
          calculator.exp(input);
        }, Error, expectedError);
      });
    });
  });

  describe('log method', () => {
    const logValidTests = [
      {
        name: 'Return 0 when input is 1 (log of 1 equals 0)',
        input: 1,
        expected: 0
      },
      {
        name: 'Return 1 when input is Euler number (natural log of e equals 1)',
        input: Math.E,
        expected: 1
      },
      {
        name: 'Return 2 when input is e squared (natural log of e² equals 2)',
        input: Math.exp(2),
        expected: 2
      },
      {
        name: 'Return natural logarithm of 10 when input is 10',
        input: 10,
        expected: Math.log(10)
      },
      {
        name: 'Return natural logarithm of 0.5 when input is 0.5',
        input: 0.5,
        expected: Math.log(0.5)
      }
    ];

    logValidTests.forEach(({ name, input, expected }) => {
      it(name, () => {
        const result = calculator.log(input);
        assert.strictEqual(result, expected);
      });
    });

    const logErrorTests = [
      {
        name: 'Throw unsupported operand type error when input is NaN',
        input: NaN,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw unsupported operand type error when input is Infinity',
        input: Infinity,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw unsupported operand type error when input is negative Infinity',
        input: -Infinity,
        expectedError: 'unsupported operand type'
      },
      {
        name: 'Throw math domain error (1) when input is 0 (log of 0 is undefined)',
        input: 0,
        expectedError: 'math domain error (1)'
      },
      {
        name: 'Throw math domain error (2) when input is negative number (-1)',
        input: -1,
        expectedError: 'math domain error (2)'
      },
      {
        name: 'Throw math domain error (2) when input is negative number (-5)',
        input: -5,
        expectedError: 'math domain error (2)'
      }
    ];

    logErrorTests.forEach(({ name, input, expectedError }) => {
      it(name, () => {
        assert.throws(() => {
          calculator.log(input);
        }, Error, expectedError);
      });
    });
  });
});
