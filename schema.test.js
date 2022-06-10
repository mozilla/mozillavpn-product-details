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

test('Internal consistency - minimum and latest entries should have a releases entry', () => {
    function check_releases(data) {
        for (const block of ["latest", "minimum"]) {
            for (const platform in data[block]) {
                let release = data[block][platform];
                console.log(`Looking for a releases entry for ${platform} ${release} (seen in ${block} block).`);
                expect(data.releases[release]).toBeDefined();
            }
        }
    }
    console.log("** Testing STAGE mozillavpn_stage.json");
    check_releases(data_stage);
    console.log("** Testing PROD mozillavpn.json");
    check_releases(data_prod);
});
