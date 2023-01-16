const Ajv = require("ajv/dist/jtd")

const schema = require('./schema.jtd.json');
const schema_release = require('./schema_release.jtd.json');
const data = require('./docs/mozillavpn.json');

const ajv = new Ajv();

test('Schema validation', () => {
    const validate = ajv.compile(schema);
    const valid = validate(data);
    if (!valid) {
        console.log(validate.errors)
    }
    expect(valid).toBe(true);

    const validate_release = ajv.compile(schema_release);
    const valid_release = validate_release(data);
    if (!valid_release) {
        console.log(validate_release.errors)
    }
    expect(valid_release).toBe(true);
})

test('Internal consistency checks', () => {
    for (const block of ["latest", "minimum"]) {
        for (const platform in data[block]) {
            let release = data[block][platform];
            console.log(`Looking for a releases entry for ${platform} ${release} (seen in ${block} block).`);
            let releases_entry = data.releases[release];
            expect(releases_entry).toBeDefined();
            console.log(`Looking for the platform ${platform} to be in ${release} entry - ${JSON.stringify(releases_entry)}`);
            expect(releases_entry.platforms.includes(platform)).toBe(true);
        }
    }
});
