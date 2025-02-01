import settings from "./Miniengine-1.0.1";

const settings = using.engine;

settings.forEach(settings => {
    setSettings(() => {
        settings.engine()
    });
});