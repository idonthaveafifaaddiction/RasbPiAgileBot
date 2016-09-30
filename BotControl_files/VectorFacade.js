var RenderFacade = (function(global, $, undefined) {
    var activeRenderer;
    var availableRenderers = { "vector2": ((global.Vector2 === undefined)? null : Vector2), "victor": ((global.Victor === undefined)? null : Victor) }

    var normalizeRenderer = function() {
        if (!activeRenderer.hasOwnProperty("reset")) {
            activeRenderer.prototype.reset = function (x, y) {
                this.x = x;
                this.y = y;

                return this;

            }
            activeRenderer.prototype.copyTo = function (v) {
                v.x = this.x;
                v.y = this.y;
            }

            activeRenderer.prototype.copyFrom = function(v) {
                this.x = v.x;
                this.y = v.y;
            }

            activeRenderer.prototype.minusEq = function (v) {
                this.x -= v.x;
                this.y -= v.y;

                return this;
            }
        }
    }

    return {
        SetActiveRenderer : function(renderer) {
            if (availableRenderers[renderer]) {
                activeRenderer = availableRenderers[renderer];
                return "Renderer Set To:" + renderer;
            }

            return "Renderer Parameter Passed is Not a Valid Renderer";
        },
        ReturnActiveRenderer : function() {
            return activeRenderer;
        },
        RenderFactory: function () {
            normalizeRenderer();

            return new activeRenderer(0, 0);
        }
    }
})(window, jQuery)