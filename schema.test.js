const Ajv = require("ajv/dist/jtd")

const schema = require('./schema.jtd.json');
const schema_release = require('./schema_release.jtd.json');
const data_stage = require('./docs/mozillavpn_stage.json');
const data_prod = require('./docs/mozillavpn.json');

const ajv = new Ajv();

test('Schema validation', () => {
    // Basic schema for both files
    const validate = ajv.compile(schema);
    const valid_stage = validate(data_stage);
    if (!valid_stage) {
        console.log(validate.errors)
    }
    const valid_prod = validate(data_prod);
    if (!valid_prod) {
        console.log(validate.errors)
    }
    expect(valid_stage).toBe(true);
    expect(valid_prod).toBe(true);

    const validate_release = ajv.compile(schema_release);
    const valid_release = validate_release(data_prod);
    if (!valid_release) {
        console.log(validate_release.errors)
    }
    expect(valid_release).toBe(true);
})

