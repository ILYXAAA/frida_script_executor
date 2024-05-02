Java.perform(function () {
    Java.use("android.view.Window").setFlags.implementation = function (flags, mask) {
        this.setFlags(flags & ~8192, mask);
    };
    Java.use("android.view.Window").addFlags.implementation = function (flags) {
        console.log("add flags");
        if (flags != 8192) {
            this.addFlags(flags);
        }
    };
    Java.use("android.view.SurfaceView").setSecure.implementation = function (isSecure) {
        console.log("call isSecure -->");
    };
});