var Mn = Object.defineProperty;
var qn = (e, t, n) => t in e ? Mn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Ge = (e, t, n) => qn(e, typeof t != "symbol" ? t + "" : t, n);
import Ht, { useState as ne, useEffect as Wt } from "react";
var tt = { exports: {} }, ge = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ot;
function Hn() {
  if (Ot) return ge;
  Ot = 1;
  var e = Ht, t = Symbol.for("react.element"), n = Symbol.for("react.fragment"), r = Object.prototype.hasOwnProperty, s = e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, a = { key: !0, ref: !0, __self: !0, __source: !0 };
  function o(l, m, h) {
    var u, y = {}, E = null, R = null;
    h !== void 0 && (E = "" + h), m.key !== void 0 && (E = "" + m.key), m.ref !== void 0 && (R = m.ref);
    for (u in m) r.call(m, u) && !a.hasOwnProperty(u) && (y[u] = m[u]);
    if (l && l.defaultProps) for (u in m = l.defaultProps, m) y[u] === void 0 && (y[u] = m[u]);
    return { $$typeof: t, type: l, key: E, ref: R, props: y, _owner: s.current };
  }
  return ge.Fragment = n, ge.jsx = o, ge.jsxs = o, ge;
}
var be = {};
/**
 * @license React
 * react-jsx-runtime.development.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Tt;
function Wn() {
  return Tt || (Tt = 1, process.env.NODE_ENV !== "production" && function() {
    var e = Ht, t = Symbol.for("react.element"), n = Symbol.for("react.portal"), r = Symbol.for("react.fragment"), s = Symbol.for("react.strict_mode"), a = Symbol.for("react.profiler"), o = Symbol.for("react.provider"), l = Symbol.for("react.context"), m = Symbol.for("react.forward_ref"), h = Symbol.for("react.suspense"), u = Symbol.for("react.suspense_list"), y = Symbol.for("react.memo"), E = Symbol.for("react.lazy"), R = Symbol.for("react.offscreen"), f = Symbol.iterator, w = "@@iterator";
    function b(i) {
      if (i === null || typeof i != "object")
        return null;
      var p = f && i[f] || i[w];
      return typeof p == "function" ? p : null;
    }
    var j = e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
    function _(i) {
      {
        for (var p = arguments.length, g = new Array(p > 1 ? p - 1 : 0), v = 1; v < p; v++)
          g[v - 1] = arguments[v];
        P("error", i, g);
      }
    }
    function P(i, p, g) {
      {
        var v = j.ReactDebugCurrentFrame, T = v.getStackAddendum();
        T !== "" && (p += "%s", g = g.concat([T]));
        var C = g.map(function(O) {
          return String(O);
        });
        C.unshift("Warning: " + p), Function.prototype.apply.call(console[i], console, C);
      }
    }
    var F = !1, H = !1, X = !1, I = !1, he = !1, Q;
    Q = Symbol.for("react.module.reference");
    function Se(i) {
      return !!(typeof i == "string" || typeof i == "function" || i === r || i === a || he || i === s || i === h || i === u || I || i === R || F || H || X || typeof i == "object" && i !== null && (i.$$typeof === E || i.$$typeof === y || i.$$typeof === o || i.$$typeof === l || i.$$typeof === m || // This needs to include all possible module reference object
      // types supported by any Flight configuration anywhere since
      // we don't know which Flight build this will end up being used
      // with.
      i.$$typeof === Q || i.getModuleId !== void 0));
    }
    function Oe(i, p, g) {
      var v = i.displayName;
      if (v)
        return v;
      var T = p.displayName || p.name || "";
      return T !== "" ? g + "(" + T + ")" : g;
    }
    function ee(i) {
      return i.displayName || "Context";
    }
    function $(i) {
      if (i == null)
        return null;
      if (typeof i.tag == "number" && _("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), typeof i == "function")
        return i.displayName || i.name || null;
      if (typeof i == "string")
        return i;
      switch (i) {
        case r:
          return "Fragment";
        case n:
          return "Portal";
        case a:
          return "Profiler";
        case s:
          return "StrictMode";
        case h:
          return "Suspense";
        case u:
          return "SuspenseList";
      }
      if (typeof i == "object")
        switch (i.$$typeof) {
          case l:
            var p = i;
            return ee(p) + ".Consumer";
          case o:
            var g = i;
            return ee(g._context) + ".Provider";
          case m:
            return Oe(i, i.render, "ForwardRef");
          case y:
            var v = i.displayName || null;
            return v !== null ? v : $(i.type) || "Memo";
          case E: {
            var T = i, C = T._payload, O = T._init;
            try {
              return $(O(C));
            } catch {
              return null;
            }
          }
        }
      return null;
    }
    var U = Object.assign, Z = 0, W, pe, V, me, Te, J, G;
    function oe() {
    }
    oe.__reactDisabledLog = !0;
    function ae() {
      {
        if (Z === 0) {
          W = console.log, pe = console.info, V = console.warn, me = console.error, Te = console.group, J = console.groupCollapsed, G = console.groupEnd;
          var i = {
            configurable: !0,
            enumerable: !0,
            value: oe,
            writable: !0
          };
          Object.defineProperties(console, {
            info: i,
            log: i,
            warn: i,
            error: i,
            group: i,
            groupCollapsed: i,
            groupEnd: i
          });
        }
        Z++;
      }
    }
    function je() {
      {
        if (Z--, Z === 0) {
          var i = {
            configurable: !0,
            enumerable: !0,
            writable: !0
          };
          Object.defineProperties(console, {
            log: U({}, i, {
              value: W
            }),
            info: U({}, i, {
              value: pe
            }),
            warn: U({}, i, {
              value: V
            }),
            error: U({}, i, {
              value: me
            }),
            group: U({}, i, {
              value: Te
            }),
            groupCollapsed: U({}, i, {
              value: J
            }),
            groupEnd: U({}, i, {
              value: G
            })
          });
        }
        Z < 0 && _("disabledDepth fell below zero. This is a bug in React. Please file an issue.");
      }
    }
    var He = j.ReactCurrentDispatcher, We;
    function _e(i, p, g) {
      {
        if (We === void 0)
          try {
            throw Error();
          } catch (T) {
            var v = T.stack.trim().match(/\n( *(at )?)/);
            We = v && v[1] || "";
          }
        return `
` + We + i;
      }
    }
    var ze = !1, Ce;
    {
      var yn = typeof WeakMap == "function" ? WeakMap : Map;
      Ce = new yn();
    }
    function ut(i, p) {
      if (!i || ze)
        return "";
      {
        var g = Ce.get(i);
        if (g !== void 0)
          return g;
      }
      var v;
      ze = !0;
      var T = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      var C;
      C = He.current, He.current = null, ae();
      try {
        if (p) {
          var O = function() {
            throw Error();
          };
          if (Object.defineProperty(O.prototype, "props", {
            set: function() {
              throw Error();
            }
          }), typeof Reflect == "object" && Reflect.construct) {
            try {
              Reflect.construct(O, []);
            } catch (B) {
              v = B;
            }
            Reflect.construct(i, [], O);
          } else {
            try {
              O.call();
            } catch (B) {
              v = B;
            }
            i.call(O.prototype);
          }
        } else {
          try {
            throw Error();
          } catch (B) {
            v = B;
          }
          i();
        }
      } catch (B) {
        if (B && v && typeof B.stack == "string") {
          for (var S = B.stack.split(`
`), L = v.stack.split(`
`), N = S.length - 1, k = L.length - 1; N >= 1 && k >= 0 && S[N] !== L[k]; )
            k--;
          for (; N >= 1 && k >= 0; N--, k--)
            if (S[N] !== L[k]) {
              if (N !== 1 || k !== 1)
                do
                  if (N--, k--, k < 0 || S[N] !== L[k]) {
                    var z = `
` + S[N].replace(" at new ", " at ");
                    return i.displayName && z.includes("<anonymous>") && (z = z.replace("<anonymous>", i.displayName)), typeof i == "function" && Ce.set(i, z), z;
                  }
                while (N >= 1 && k >= 0);
              break;
            }
        }
      } finally {
        ze = !1, He.current = C, je(), Error.prepareStackTrace = T;
      }
      var le = i ? i.displayName || i.name : "", te = le ? _e(le) : "";
      return typeof i == "function" && Ce.set(i, te), te;
    }
    function gn(i, p, g) {
      return ut(i, !1);
    }
    function bn(i) {
      var p = i.prototype;
      return !!(p && p.isReactComponent);
    }
    function Ae(i, p, g) {
      if (i == null)
        return "";
      if (typeof i == "function")
        return ut(i, bn(i));
      if (typeof i == "string")
        return _e(i);
      switch (i) {
        case h:
          return _e("Suspense");
        case u:
          return _e("SuspenseList");
      }
      if (typeof i == "object")
        switch (i.$$typeof) {
          case m:
            return gn(i.render);
          case y:
            return Ae(i.type, p, g);
          case E: {
            var v = i, T = v._payload, C = v._init;
            try {
              return Ae(C(T), p, g);
            } catch {
            }
          }
        }
      return "";
    }
    var ye = Object.prototype.hasOwnProperty, ft = {}, dt = j.ReactDebugCurrentFrame;
    function Ne(i) {
      if (i) {
        var p = i._owner, g = Ae(i.type, i._source, p ? p.type : null);
        dt.setExtraStackFrame(g);
      } else
        dt.setExtraStackFrame(null);
    }
    function wn(i, p, g, v, T) {
      {
        var C = Function.call.bind(ye);
        for (var O in i)
          if (C(i, O)) {
            var S = void 0;
            try {
              if (typeof i[O] != "function") {
                var L = Error((v || "React class") + ": " + g + " type `" + O + "` is invalid; it must be a function, usually from the `prop-types` package, but received `" + typeof i[O] + "`.This often happens because of typos such as `PropTypes.function` instead of `PropTypes.func`.");
                throw L.name = "Invariant Violation", L;
              }
              S = i[O](p, O, v, g, null, "SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED");
            } catch (N) {
              S = N;
            }
            S && !(S instanceof Error) && (Ne(T), _("%s: type specification of %s `%s` is invalid; the type checker function must return `null` or an `Error` but returned a %s. You may have forgotten to pass an argument to the type checker creator (arrayOf, instanceOf, objectOf, oneOf, oneOfType, and shape all require an argument).", v || "React class", g, O, typeof S), Ne(null)), S instanceof Error && !(S.message in ft) && (ft[S.message] = !0, Ne(T), _("Failed %s type: %s", g, S.message), Ne(null));
          }
      }
    }
    var vn = Array.isArray;
    function Ve(i) {
      return vn(i);
    }
    function En(i) {
      {
        var p = typeof Symbol == "function" && Symbol.toStringTag, g = p && i[Symbol.toStringTag] || i.constructor.name || "Object";
        return g;
      }
    }
    function Rn(i) {
      try {
        return ht(i), !1;
      } catch {
        return !0;
      }
    }
    function ht(i) {
      return "" + i;
    }
    function pt(i) {
      if (Rn(i))
        return _("The provided key is an unsupported type %s. This value must be coerced to a string before before using it here.", En(i)), ht(i);
    }
    var mt = j.ReactCurrentOwner, xn = {
      key: !0,
      ref: !0,
      __self: !0,
      __source: !0
    }, yt, gt;
    function Sn(i) {
      if (ye.call(i, "ref")) {
        var p = Object.getOwnPropertyDescriptor(i, "ref").get;
        if (p && p.isReactWarning)
          return !1;
      }
      return i.ref !== void 0;
    }
    function On(i) {
      if (ye.call(i, "key")) {
        var p = Object.getOwnPropertyDescriptor(i, "key").get;
        if (p && p.isReactWarning)
          return !1;
      }
      return i.key !== void 0;
    }
    function Tn(i, p) {
      typeof i.ref == "string" && mt.current;
    }
    function jn(i, p) {
      {
        var g = function() {
          yt || (yt = !0, _("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", p));
        };
        g.isReactWarning = !0, Object.defineProperty(i, "key", {
          get: g,
          configurable: !0
        });
      }
    }
    function _n(i, p) {
      {
        var g = function() {
          gt || (gt = !0, _("%s: `ref` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://reactjs.org/link/special-props)", p));
        };
        g.isReactWarning = !0, Object.defineProperty(i, "ref", {
          get: g,
          configurable: !0
        });
      }
    }
    var Cn = function(i, p, g, v, T, C, O) {
      var S = {
        // This tag allows us to uniquely identify this as a React Element
        $$typeof: t,
        // Built-in properties that belong on the element
        type: i,
        key: p,
        ref: g,
        props: O,
        // Record the component responsible for creating this element.
        _owner: C
      };
      return S._store = {}, Object.defineProperty(S._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: !1
      }), Object.defineProperty(S, "_self", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: v
      }), Object.defineProperty(S, "_source", {
        configurable: !1,
        enumerable: !1,
        writable: !1,
        value: T
      }), Object.freeze && (Object.freeze(S.props), Object.freeze(S)), S;
    };
    function An(i, p, g, v, T) {
      {
        var C, O = {}, S = null, L = null;
        g !== void 0 && (pt(g), S = "" + g), On(p) && (pt(p.key), S = "" + p.key), Sn(p) && (L = p.ref, Tn(p, T));
        for (C in p)
          ye.call(p, C) && !xn.hasOwnProperty(C) && (O[C] = p[C]);
        if (i && i.defaultProps) {
          var N = i.defaultProps;
          for (C in N)
            O[C] === void 0 && (O[C] = N[C]);
        }
        if (S || L) {
          var k = typeof i == "function" ? i.displayName || i.name || "Unknown" : i;
          S && jn(O, k), L && _n(O, k);
        }
        return Cn(i, S, L, T, v, mt.current, O);
      }
    }
    var Je = j.ReactCurrentOwner, bt = j.ReactDebugCurrentFrame;
    function ce(i) {
      if (i) {
        var p = i._owner, g = Ae(i.type, i._source, p ? p.type : null);
        bt.setExtraStackFrame(g);
      } else
        bt.setExtraStackFrame(null);
    }
    var Ke;
    Ke = !1;
    function Ye(i) {
      return typeof i == "object" && i !== null && i.$$typeof === t;
    }
    function wt() {
      {
        if (Je.current) {
          var i = $(Je.current.type);
          if (i)
            return `

Check the render method of \`` + i + "`.";
        }
        return "";
      }
    }
    function Nn(i) {
      return "";
    }
    var vt = {};
    function Pn(i) {
      {
        var p = wt();
        if (!p) {
          var g = typeof i == "string" ? i : i.displayName || i.name;
          g && (p = `

Check the top-level render call using <` + g + ">.");
        }
        return p;
      }
    }
    function Et(i, p) {
      {
        if (!i._store || i._store.validated || i.key != null)
          return;
        i._store.validated = !0;
        var g = Pn(p);
        if (vt[g])
          return;
        vt[g] = !0;
        var v = "";
        i && i._owner && i._owner !== Je.current && (v = " It was passed a child from " + $(i._owner.type) + "."), ce(i), _('Each child in a list should have a unique "key" prop.%s%s See https://reactjs.org/link/warning-keys for more information.', g, v), ce(null);
      }
    }
    function Rt(i, p) {
      {
        if (typeof i != "object")
          return;
        if (Ve(i))
          for (var g = 0; g < i.length; g++) {
            var v = i[g];
            Ye(v) && Et(v, p);
          }
        else if (Ye(i))
          i._store && (i._store.validated = !0);
        else if (i) {
          var T = b(i);
          if (typeof T == "function" && T !== i.entries)
            for (var C = T.call(i), O; !(O = C.next()).done; )
              Ye(O.value) && Et(O.value, p);
        }
      }
    }
    function kn(i) {
      {
        var p = i.type;
        if (p == null || typeof p == "string")
          return;
        var g;
        if (typeof p == "function")
          g = p.propTypes;
        else if (typeof p == "object" && (p.$$typeof === m || // Note: Memo only checks outer props here.
        // Inner props are checked in the reconciler.
        p.$$typeof === y))
          g = p.propTypes;
        else
          return;
        if (g) {
          var v = $(p);
          wn(g, i.props, "prop", v, i);
        } else if (p.PropTypes !== void 0 && !Ke) {
          Ke = !0;
          var T = $(p);
          _("Component %s declared `PropTypes` instead of `propTypes`. Did you misspell the property assignment?", T || "Unknown");
        }
        typeof p.getDefaultProps == "function" && !p.getDefaultProps.isReactClassApproved && _("getDefaultProps is only used on classic React.createClass definitions. Use a static property named `defaultProps` instead.");
      }
    }
    function Fn(i) {
      {
        for (var p = Object.keys(i.props), g = 0; g < p.length; g++) {
          var v = p[g];
          if (v !== "children" && v !== "key") {
            ce(i), _("Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.", v), ce(null);
            break;
          }
        }
        i.ref !== null && (ce(i), _("Invalid attribute `ref` supplied to `React.Fragment`."), ce(null));
      }
    }
    var xt = {};
    function St(i, p, g, v, T, C) {
      {
        var O = Se(i);
        if (!O) {
          var S = "";
          (i === void 0 || typeof i == "object" && i !== null && Object.keys(i).length === 0) && (S += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.");
          var L = Nn();
          L ? S += L : S += wt();
          var N;
          i === null ? N = "null" : Ve(i) ? N = "array" : i !== void 0 && i.$$typeof === t ? (N = "<" + ($(i.type) || "Unknown") + " />", S = " Did you accidentally export a JSX literal instead of a component?") : N = typeof i, _("React.jsx: type is invalid -- expected a string (for built-in components) or a class/function (for composite components) but got: %s.%s", N, S);
        }
        var k = An(i, p, g, T, C);
        if (k == null)
          return k;
        if (O) {
          var z = p.children;
          if (z !== void 0)
            if (v)
              if (Ve(z)) {
                for (var le = 0; le < z.length; le++)
                  Rt(z[le], i);
                Object.freeze && Object.freeze(z);
              } else
                _("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
            else
              Rt(z, i);
        }
        if (ye.call(p, "key")) {
          var te = $(i), B = Object.keys(p).filter(function(Bn) {
            return Bn !== "key";
          }), Xe = B.length > 0 ? "{key: someKey, " + B.join(": ..., ") + ": ...}" : "{key: someKey}";
          if (!xt[te + Xe]) {
            var $n = B.length > 0 ? "{" + B.join(": ..., ") + ": ...}" : "{}";
            _(`A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`, Xe, te, $n, te), xt[te + Xe] = !0;
          }
        }
        return i === r ? Fn(k) : kn(k), k;
      }
    }
    function Dn(i, p, g) {
      return St(i, p, g, !0);
    }
    function Un(i, p, g) {
      return St(i, p, g, !1);
    }
    var Ln = Un, In = Dn;
    be.Fragment = r, be.jsx = Ln, be.jsxs = In;
  }()), be;
}
process.env.NODE_ENV === "production" ? tt.exports = Hn() : tt.exports = Wn();
var d = tt.exports;
function zt(e, t) {
  return function() {
    return e.apply(t, arguments);
  };
}
const { toString: zn } = Object.prototype, { getPrototypeOf: ot } = Object, { iterator: Ie, toStringTag: Vt } = Symbol, $e = /* @__PURE__ */ ((e) => (t) => {
  const n = zn.call(t);
  return e[n] || (e[n] = n.slice(8, -1).toLowerCase());
})(/* @__PURE__ */ Object.create(null)), K = (e) => (e = e.toLowerCase(), (t) => $e(t) === e), Be = (e) => (t) => typeof t === e, { isArray: fe } = Array, ue = Be("undefined");
function ve(e) {
  return e !== null && !ue(e) && e.constructor !== null && !ue(e.constructor) && M(e.constructor.isBuffer) && e.constructor.isBuffer(e);
}
const Jt = K("ArrayBuffer");
function Vn(e) {
  let t;
  return typeof ArrayBuffer < "u" && ArrayBuffer.isView ? t = ArrayBuffer.isView(e) : t = e && e.buffer && Jt(e.buffer), t;
}
const Jn = Be("string"), M = Be("function"), Kt = Be("number"), Ee = (e) => e !== null && typeof e == "object", Kn = (e) => e === !0 || e === !1, ke = (e) => {
  if ($e(e) !== "object")
    return !1;
  const t = ot(e);
  return (t === null || t === Object.prototype || Object.getPrototypeOf(t) === null) && !(Vt in e) && !(Ie in e);
}, Yn = (e) => {
  if (!Ee(e) || ve(e))
    return !1;
  try {
    return Object.keys(e).length === 0 && Object.getPrototypeOf(e) === Object.prototype;
  } catch {
    return !1;
  }
}, Xn = K("Date"), Gn = K("File"), Zn = K("Blob"), Qn = K("FileList"), er = (e) => Ee(e) && M(e.pipe), tr = (e) => {
  let t;
  return e && (typeof FormData == "function" && e instanceof FormData || M(e.append) && ((t = $e(e)) === "formdata" || // detect form-data instance
  t === "object" && M(e.toString) && e.toString() === "[object FormData]"));
}, nr = K("URLSearchParams"), [rr, sr, ir, or] = ["ReadableStream", "Request", "Response", "Headers"].map(K), ar = (e) => e.trim ? e.trim() : e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "");
function Re(e, t, { allOwnKeys: n = !1 } = {}) {
  if (e === null || typeof e > "u")
    return;
  let r, s;
  if (typeof e != "object" && (e = [e]), fe(e))
    for (r = 0, s = e.length; r < s; r++)
      t.call(null, e[r], r, e);
  else {
    if (ve(e))
      return;
    const a = n ? Object.getOwnPropertyNames(e) : Object.keys(e), o = a.length;
    let l;
    for (r = 0; r < o; r++)
      l = a[r], t.call(null, e[l], l, e);
  }
}
function Yt(e, t) {
  if (ve(e))
    return null;
  t = t.toLowerCase();
  const n = Object.keys(e);
  let r = n.length, s;
  for (; r-- > 0; )
    if (s = n[r], t === s.toLowerCase())
      return s;
  return null;
}
const re = typeof globalThis < "u" ? globalThis : typeof self < "u" ? self : typeof window < "u" ? window : global, Xt = (e) => !ue(e) && e !== re;
function nt() {
  const { caseless: e, skipUndefined: t } = Xt(this) && this || {}, n = {}, r = (s, a) => {
    const o = e && Yt(n, a) || a;
    ke(n[o]) && ke(s) ? n[o] = nt(n[o], s) : ke(s) ? n[o] = nt({}, s) : fe(s) ? n[o] = s.slice() : (!t || !ue(s)) && (n[o] = s);
  };
  for (let s = 0, a = arguments.length; s < a; s++)
    arguments[s] && Re(arguments[s], r);
  return n;
}
const cr = (e, t, n, { allOwnKeys: r } = {}) => (Re(t, (s, a) => {
  n && M(s) ? e[a] = zt(s, n) : e[a] = s;
}, { allOwnKeys: r }), e), lr = (e) => (e.charCodeAt(0) === 65279 && (e = e.slice(1)), e), ur = (e, t, n, r) => {
  e.prototype = Object.create(t.prototype, r), e.prototype.constructor = e, Object.defineProperty(e, "super", {
    value: t.prototype
  }), n && Object.assign(e.prototype, n);
}, fr = (e, t, n, r) => {
  let s, a, o;
  const l = {};
  if (t = t || {}, e == null) return t;
  do {
    for (s = Object.getOwnPropertyNames(e), a = s.length; a-- > 0; )
      o = s[a], (!r || r(o, e, t)) && !l[o] && (t[o] = e[o], l[o] = !0);
    e = n !== !1 && ot(e);
  } while (e && (!n || n(e, t)) && e !== Object.prototype);
  return t;
}, dr = (e, t, n) => {
  e = String(e), (n === void 0 || n > e.length) && (n = e.length), n -= t.length;
  const r = e.indexOf(t, n);
  return r !== -1 && r === n;
}, hr = (e) => {
  if (!e) return null;
  if (fe(e)) return e;
  let t = e.length;
  if (!Kt(t)) return null;
  const n = new Array(t);
  for (; t-- > 0; )
    n[t] = e[t];
  return n;
}, pr = /* @__PURE__ */ ((e) => (t) => e && t instanceof e)(typeof Uint8Array < "u" && ot(Uint8Array)), mr = (e, t) => {
  const r = (e && e[Ie]).call(e);
  let s;
  for (; (s = r.next()) && !s.done; ) {
    const a = s.value;
    t.call(e, a[0], a[1]);
  }
}, yr = (e, t) => {
  let n;
  const r = [];
  for (; (n = e.exec(t)) !== null; )
    r.push(n);
  return r;
}, gr = K("HTMLFormElement"), br = (e) => e.toLowerCase().replace(
  /[-_\s]([a-z\d])(\w*)/g,
  function(n, r, s) {
    return r.toUpperCase() + s;
  }
), jt = (({ hasOwnProperty: e }) => (t, n) => e.call(t, n))(Object.prototype), wr = K("RegExp"), Gt = (e, t) => {
  const n = Object.getOwnPropertyDescriptors(e), r = {};
  Re(n, (s, a) => {
    let o;
    (o = t(s, a, e)) !== !1 && (r[a] = o || s);
  }), Object.defineProperties(e, r);
}, vr = (e) => {
  Gt(e, (t, n) => {
    if (M(e) && ["arguments", "caller", "callee"].indexOf(n) !== -1)
      return !1;
    const r = e[n];
    if (M(r)) {
      if (t.enumerable = !1, "writable" in t) {
        t.writable = !1;
        return;
      }
      t.set || (t.set = () => {
        throw Error("Can not rewrite read-only method '" + n + "'");
      });
    }
  });
}, Er = (e, t) => {
  const n = {}, r = (s) => {
    s.forEach((a) => {
      n[a] = !0;
    });
  };
  return fe(e) ? r(e) : r(String(e).split(t)), n;
}, Rr = () => {
}, xr = (e, t) => e != null && Number.isFinite(e = +e) ? e : t;
function Sr(e) {
  return !!(e && M(e.append) && e[Vt] === "FormData" && e[Ie]);
}
const Or = (e) => {
  const t = new Array(10), n = (r, s) => {
    if (Ee(r)) {
      if (t.indexOf(r) >= 0)
        return;
      if (ve(r))
        return r;
      if (!("toJSON" in r)) {
        t[s] = r;
        const a = fe(r) ? [] : {};
        return Re(r, (o, l) => {
          const m = n(o, s + 1);
          !ue(m) && (a[l] = m);
        }), t[s] = void 0, a;
      }
    }
    return r;
  };
  return n(e, 0);
}, Tr = K("AsyncFunction"), jr = (e) => e && (Ee(e) || M(e)) && M(e.then) && M(e.catch), Zt = ((e, t) => e ? setImmediate : t ? ((n, r) => (re.addEventListener("message", ({ source: s, data: a }) => {
  s === re && a === n && r.length && r.shift()();
}, !1), (s) => {
  r.push(s), re.postMessage(n, "*");
}))(`axios@${Math.random()}`, []) : (n) => setTimeout(n))(
  typeof setImmediate == "function",
  M(re.postMessage)
), _r = typeof queueMicrotask < "u" ? queueMicrotask.bind(re) : typeof process < "u" && process.nextTick || Zt, Cr = (e) => e != null && M(e[Ie]), c = {
  isArray: fe,
  isArrayBuffer: Jt,
  isBuffer: ve,
  isFormData: tr,
  isArrayBufferView: Vn,
  isString: Jn,
  isNumber: Kt,
  isBoolean: Kn,
  isObject: Ee,
  isPlainObject: ke,
  isEmptyObject: Yn,
  isReadableStream: rr,
  isRequest: sr,
  isResponse: ir,
  isHeaders: or,
  isUndefined: ue,
  isDate: Xn,
  isFile: Gn,
  isBlob: Zn,
  isRegExp: wr,
  isFunction: M,
  isStream: er,
  isURLSearchParams: nr,
  isTypedArray: pr,
  isFileList: Qn,
  forEach: Re,
  merge: nt,
  extend: cr,
  trim: ar,
  stripBOM: lr,
  inherits: ur,
  toFlatObject: fr,
  kindOf: $e,
  kindOfTest: K,
  endsWith: dr,
  toArray: hr,
  forEachEntry: mr,
  matchAll: yr,
  isHTMLForm: gr,
  hasOwnProperty: jt,
  hasOwnProp: jt,
  // an alias to avoid ESLint no-prototype-builtins detection
  reduceDescriptors: Gt,
  freezeMethods: vr,
  toObjectSet: Er,
  toCamelCase: br,
  noop: Rr,
  toFiniteNumber: xr,
  findKey: Yt,
  global: re,
  isContextDefined: Xt,
  isSpecCompliantForm: Sr,
  toJSONObject: Or,
  isAsyncFn: Tr,
  isThenable: jr,
  setImmediate: Zt,
  asap: _r,
  isIterable: Cr
};
function x(e, t, n, r, s) {
  Error.call(this), Error.captureStackTrace ? Error.captureStackTrace(this, this.constructor) : this.stack = new Error().stack, this.message = e, this.name = "AxiosError", t && (this.code = t), n && (this.config = n), r && (this.request = r), s && (this.response = s, this.status = s.status ? s.status : null);
}
c.inherits(x, Error, {
  toJSON: function() {
    return {
      // Standard
      message: this.message,
      name: this.name,
      // Microsoft
      description: this.description,
      number: this.number,
      // Mozilla
      fileName: this.fileName,
      lineNumber: this.lineNumber,
      columnNumber: this.columnNumber,
      stack: this.stack,
      // Axios
      config: c.toJSONObject(this.config),
      code: this.code,
      status: this.status
    };
  }
});
const Qt = x.prototype, en = {};
[
  "ERR_BAD_OPTION_VALUE",
  "ERR_BAD_OPTION",
  "ECONNABORTED",
  "ETIMEDOUT",
  "ERR_NETWORK",
  "ERR_FR_TOO_MANY_REDIRECTS",
  "ERR_DEPRECATED",
  "ERR_BAD_RESPONSE",
  "ERR_BAD_REQUEST",
  "ERR_CANCELED",
  "ERR_NOT_SUPPORT",
  "ERR_INVALID_URL"
  // eslint-disable-next-line func-names
].forEach((e) => {
  en[e] = { value: e };
});
Object.defineProperties(x, en);
Object.defineProperty(Qt, "isAxiosError", { value: !0 });
x.from = (e, t, n, r, s, a) => {
  const o = Object.create(Qt);
  c.toFlatObject(e, o, function(u) {
    return u !== Error.prototype;
  }, (h) => h !== "isAxiosError");
  const l = e && e.message ? e.message : "Error", m = t == null && e ? e.code : t;
  return x.call(o, l, m, n, r, s), e && o.cause == null && Object.defineProperty(o, "cause", { value: e, configurable: !0 }), o.name = e && e.name || "Error", a && Object.assign(o, a), o;
};
const Ar = null;
function rt(e) {
  return c.isPlainObject(e) || c.isArray(e);
}
function tn(e) {
  return c.endsWith(e, "[]") ? e.slice(0, -2) : e;
}
function _t(e, t, n) {
  return e ? e.concat(t).map(function(s, a) {
    return s = tn(s), !n && a ? "[" + s + "]" : s;
  }).join(n ? "." : "") : t;
}
function Nr(e) {
  return c.isArray(e) && !e.some(rt);
}
const Pr = c.toFlatObject(c, {}, null, function(t) {
  return /^is[A-Z]/.test(t);
});
function Me(e, t, n) {
  if (!c.isObject(e))
    throw new TypeError("target must be an object");
  t = t || new FormData(), n = c.toFlatObject(n, {
    metaTokens: !0,
    dots: !1,
    indexes: !1
  }, !1, function(w, b) {
    return !c.isUndefined(b[w]);
  });
  const r = n.metaTokens, s = n.visitor || u, a = n.dots, o = n.indexes, m = (n.Blob || typeof Blob < "u" && Blob) && c.isSpecCompliantForm(t);
  if (!c.isFunction(s))
    throw new TypeError("visitor must be a function");
  function h(f) {
    if (f === null) return "";
    if (c.isDate(f))
      return f.toISOString();
    if (c.isBoolean(f))
      return f.toString();
    if (!m && c.isBlob(f))
      throw new x("Blob is not supported. Use a Buffer instead.");
    return c.isArrayBuffer(f) || c.isTypedArray(f) ? m && typeof Blob == "function" ? new Blob([f]) : Buffer.from(f) : f;
  }
  function u(f, w, b) {
    let j = f;
    if (f && !b && typeof f == "object") {
      if (c.endsWith(w, "{}"))
        w = r ? w : w.slice(0, -2), f = JSON.stringify(f);
      else if (c.isArray(f) && Nr(f) || (c.isFileList(f) || c.endsWith(w, "[]")) && (j = c.toArray(f)))
        return w = tn(w), j.forEach(function(P, F) {
          !(c.isUndefined(P) || P === null) && t.append(
            // eslint-disable-next-line no-nested-ternary
            o === !0 ? _t([w], F, a) : o === null ? w : w + "[]",
            h(P)
          );
        }), !1;
    }
    return rt(f) ? !0 : (t.append(_t(b, w, a), h(f)), !1);
  }
  const y = [], E = Object.assign(Pr, {
    defaultVisitor: u,
    convertValue: h,
    isVisitable: rt
  });
  function R(f, w) {
    if (!c.isUndefined(f)) {
      if (y.indexOf(f) !== -1)
        throw Error("Circular reference detected in " + w.join("."));
      y.push(f), c.forEach(f, function(j, _) {
        (!(c.isUndefined(j) || j === null) && s.call(
          t,
          j,
          c.isString(_) ? _.trim() : _,
          w,
          E
        )) === !0 && R(j, w ? w.concat(_) : [_]);
      }), y.pop();
    }
  }
  if (!c.isObject(e))
    throw new TypeError("data must be an object");
  return R(e), t;
}
function Ct(e) {
  const t = {
    "!": "%21",
    "'": "%27",
    "(": "%28",
    ")": "%29",
    "~": "%7E",
    "%20": "+",
    "%00": "\0"
  };
  return encodeURIComponent(e).replace(/[!'()~]|%20|%00/g, function(r) {
    return t[r];
  });
}
function at(e, t) {
  this._pairs = [], e && Me(e, this, t);
}
const nn = at.prototype;
nn.append = function(t, n) {
  this._pairs.push([t, n]);
};
nn.toString = function(t) {
  const n = t ? function(r) {
    return t.call(this, r, Ct);
  } : Ct;
  return this._pairs.map(function(s) {
    return n(s[0]) + "=" + n(s[1]);
  }, "").join("&");
};
function kr(e) {
  return encodeURIComponent(e).replace(/%3A/gi, ":").replace(/%24/g, "$").replace(/%2C/gi, ",").replace(/%20/g, "+");
}
function rn(e, t, n) {
  if (!t)
    return e;
  const r = n && n.encode || kr;
  c.isFunction(n) && (n = {
    serialize: n
  });
  const s = n && n.serialize;
  let a;
  if (s ? a = s(t, n) : a = c.isURLSearchParams(t) ? t.toString() : new at(t, n).toString(r), a) {
    const o = e.indexOf("#");
    o !== -1 && (e = e.slice(0, o)), e += (e.indexOf("?") === -1 ? "?" : "&") + a;
  }
  return e;
}
class At {
  constructor() {
    this.handlers = [];
  }
  /**
   * Add a new interceptor to the stack
   *
   * @param {Function} fulfilled The function to handle `then` for a `Promise`
   * @param {Function} rejected The function to handle `reject` for a `Promise`
   *
   * @return {Number} An ID used to remove interceptor later
   */
  use(t, n, r) {
    return this.handlers.push({
      fulfilled: t,
      rejected: n,
      synchronous: r ? r.synchronous : !1,
      runWhen: r ? r.runWhen : null
    }), this.handlers.length - 1;
  }
  /**
   * Remove an interceptor from the stack
   *
   * @param {Number} id The ID that was returned by `use`
   *
   * @returns {void}
   */
  eject(t) {
    this.handlers[t] && (this.handlers[t] = null);
  }
  /**
   * Clear all interceptors from the stack
   *
   * @returns {void}
   */
  clear() {
    this.handlers && (this.handlers = []);
  }
  /**
   * Iterate over all the registered interceptors
   *
   * This method is particularly useful for skipping over any
   * interceptors that may have become `null` calling `eject`.
   *
   * @param {Function} fn The function to call for each interceptor
   *
   * @returns {void}
   */
  forEach(t) {
    c.forEach(this.handlers, function(r) {
      r !== null && t(r);
    });
  }
}
const sn = {
  silentJSONParsing: !0,
  forcedJSONParsing: !0,
  clarifyTimeoutError: !1
}, Fr = typeof URLSearchParams < "u" ? URLSearchParams : at, Dr = typeof FormData < "u" ? FormData : null, Ur = typeof Blob < "u" ? Blob : null, Lr = {
  isBrowser: !0,
  classes: {
    URLSearchParams: Fr,
    FormData: Dr,
    Blob: Ur
  },
  protocols: ["http", "https", "file", "blob", "url", "data"]
}, ct = typeof window < "u" && typeof document < "u", st = typeof navigator == "object" && navigator || void 0, Ir = ct && (!st || ["ReactNative", "NativeScript", "NS"].indexOf(st.product) < 0), $r = typeof WorkerGlobalScope < "u" && // eslint-disable-next-line no-undef
self instanceof WorkerGlobalScope && typeof self.importScripts == "function", Br = ct && window.location.href || "http://localhost", Mr = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  hasBrowserEnv: ct,
  hasStandardBrowserEnv: Ir,
  hasStandardBrowserWebWorkerEnv: $r,
  navigator: st,
  origin: Br
}, Symbol.toStringTag, { value: "Module" })), D = {
  ...Mr,
  ...Lr
};
function qr(e, t) {
  return Me(e, new D.classes.URLSearchParams(), {
    visitor: function(n, r, s, a) {
      return D.isNode && c.isBuffer(n) ? (this.append(r, n.toString("base64")), !1) : a.defaultVisitor.apply(this, arguments);
    },
    ...t
  });
}
function Hr(e) {
  return c.matchAll(/\w+|\[(\w*)]/g, e).map((t) => t[0] === "[]" ? "" : t[1] || t[0]);
}
function Wr(e) {
  const t = {}, n = Object.keys(e);
  let r;
  const s = n.length;
  let a;
  for (r = 0; r < s; r++)
    a = n[r], t[a] = e[a];
  return t;
}
function on(e) {
  function t(n, r, s, a) {
    let o = n[a++];
    if (o === "__proto__") return !0;
    const l = Number.isFinite(+o), m = a >= n.length;
    return o = !o && c.isArray(s) ? s.length : o, m ? (c.hasOwnProp(s, o) ? s[o] = [s[o], r] : s[o] = r, !l) : ((!s[o] || !c.isObject(s[o])) && (s[o] = []), t(n, r, s[o], a) && c.isArray(s[o]) && (s[o] = Wr(s[o])), !l);
  }
  if (c.isFormData(e) && c.isFunction(e.entries)) {
    const n = {};
    return c.forEachEntry(e, (r, s) => {
      t(Hr(r), s, n, 0);
    }), n;
  }
  return null;
}
function zr(e, t, n) {
  if (c.isString(e))
    try {
      return (t || JSON.parse)(e), c.trim(e);
    } catch (r) {
      if (r.name !== "SyntaxError")
        throw r;
    }
  return (n || JSON.stringify)(e);
}
const xe = {
  transitional: sn,
  adapter: ["xhr", "http", "fetch"],
  transformRequest: [function(t, n) {
    const r = n.getContentType() || "", s = r.indexOf("application/json") > -1, a = c.isObject(t);
    if (a && c.isHTMLForm(t) && (t = new FormData(t)), c.isFormData(t))
      return s ? JSON.stringify(on(t)) : t;
    if (c.isArrayBuffer(t) || c.isBuffer(t) || c.isStream(t) || c.isFile(t) || c.isBlob(t) || c.isReadableStream(t))
      return t;
    if (c.isArrayBufferView(t))
      return t.buffer;
    if (c.isURLSearchParams(t))
      return n.setContentType("application/x-www-form-urlencoded;charset=utf-8", !1), t.toString();
    let l;
    if (a) {
      if (r.indexOf("application/x-www-form-urlencoded") > -1)
        return qr(t, this.formSerializer).toString();
      if ((l = c.isFileList(t)) || r.indexOf("multipart/form-data") > -1) {
        const m = this.env && this.env.FormData;
        return Me(
          l ? { "files[]": t } : t,
          m && new m(),
          this.formSerializer
        );
      }
    }
    return a || s ? (n.setContentType("application/json", !1), zr(t)) : t;
  }],
  transformResponse: [function(t) {
    const n = this.transitional || xe.transitional, r = n && n.forcedJSONParsing, s = this.responseType === "json";
    if (c.isResponse(t) || c.isReadableStream(t))
      return t;
    if (t && c.isString(t) && (r && !this.responseType || s)) {
      const o = !(n && n.silentJSONParsing) && s;
      try {
        return JSON.parse(t, this.parseReviver);
      } catch (l) {
        if (o)
          throw l.name === "SyntaxError" ? x.from(l, x.ERR_BAD_RESPONSE, this, null, this.response) : l;
      }
    }
    return t;
  }],
  /**
   * A timeout in milliseconds to abort a request. If set to 0 (default) a
   * timeout is not created.
   */
  timeout: 0,
  xsrfCookieName: "XSRF-TOKEN",
  xsrfHeaderName: "X-XSRF-TOKEN",
  maxContentLength: -1,
  maxBodyLength: -1,
  env: {
    FormData: D.classes.FormData,
    Blob: D.classes.Blob
  },
  validateStatus: function(t) {
    return t >= 200 && t < 300;
  },
  headers: {
    common: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": void 0
    }
  }
};
c.forEach(["delete", "get", "head", "post", "put", "patch"], (e) => {
  xe.headers[e] = {};
});
const Vr = c.toObjectSet([
  "age",
  "authorization",
  "content-length",
  "content-type",
  "etag",
  "expires",
  "from",
  "host",
  "if-modified-since",
  "if-unmodified-since",
  "last-modified",
  "location",
  "max-forwards",
  "proxy-authorization",
  "referer",
  "retry-after",
  "user-agent"
]), Jr = (e) => {
  const t = {};
  let n, r, s;
  return e && e.split(`
`).forEach(function(o) {
    s = o.indexOf(":"), n = o.substring(0, s).trim().toLowerCase(), r = o.substring(s + 1).trim(), !(!n || t[n] && Vr[n]) && (n === "set-cookie" ? t[n] ? t[n].push(r) : t[n] = [r] : t[n] = t[n] ? t[n] + ", " + r : r);
  }), t;
}, Nt = Symbol("internals");
function we(e) {
  return e && String(e).trim().toLowerCase();
}
function Fe(e) {
  return e === !1 || e == null ? e : c.isArray(e) ? e.map(Fe) : String(e);
}
function Kr(e) {
  const t = /* @__PURE__ */ Object.create(null), n = /([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;
  let r;
  for (; r = n.exec(e); )
    t[r[1]] = r[2];
  return t;
}
const Yr = (e) => /^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(e.trim());
function Ze(e, t, n, r, s) {
  if (c.isFunction(r))
    return r.call(this, t, n);
  if (s && (t = n), !!c.isString(t)) {
    if (c.isString(r))
      return t.indexOf(r) !== -1;
    if (c.isRegExp(r))
      return r.test(t);
  }
}
function Xr(e) {
  return e.trim().toLowerCase().replace(/([a-z\d])(\w*)/g, (t, n, r) => n.toUpperCase() + r);
}
function Gr(e, t) {
  const n = c.toCamelCase(" " + t);
  ["get", "set", "has"].forEach((r) => {
    Object.defineProperty(e, r + n, {
      value: function(s, a, o) {
        return this[r].call(this, t, s, a, o);
      },
      configurable: !0
    });
  });
}
let q = class {
  constructor(t) {
    t && this.set(t);
  }
  set(t, n, r) {
    const s = this;
    function a(l, m, h) {
      const u = we(m);
      if (!u)
        throw new Error("header name must be a non-empty string");
      const y = c.findKey(s, u);
      (!y || s[y] === void 0 || h === !0 || h === void 0 && s[y] !== !1) && (s[y || m] = Fe(l));
    }
    const o = (l, m) => c.forEach(l, (h, u) => a(h, u, m));
    if (c.isPlainObject(t) || t instanceof this.constructor)
      o(t, n);
    else if (c.isString(t) && (t = t.trim()) && !Yr(t))
      o(Jr(t), n);
    else if (c.isObject(t) && c.isIterable(t)) {
      let l = {}, m, h;
      for (const u of t) {
        if (!c.isArray(u))
          throw TypeError("Object iterator must return a key-value pair");
        l[h = u[0]] = (m = l[h]) ? c.isArray(m) ? [...m, u[1]] : [m, u[1]] : u[1];
      }
      o(l, n);
    } else
      t != null && a(n, t, r);
    return this;
  }
  get(t, n) {
    if (t = we(t), t) {
      const r = c.findKey(this, t);
      if (r) {
        const s = this[r];
        if (!n)
          return s;
        if (n === !0)
          return Kr(s);
        if (c.isFunction(n))
          return n.call(this, s, r);
        if (c.isRegExp(n))
          return n.exec(s);
        throw new TypeError("parser must be boolean|regexp|function");
      }
    }
  }
  has(t, n) {
    if (t = we(t), t) {
      const r = c.findKey(this, t);
      return !!(r && this[r] !== void 0 && (!n || Ze(this, this[r], r, n)));
    }
    return !1;
  }
  delete(t, n) {
    const r = this;
    let s = !1;
    function a(o) {
      if (o = we(o), o) {
        const l = c.findKey(r, o);
        l && (!n || Ze(r, r[l], l, n)) && (delete r[l], s = !0);
      }
    }
    return c.isArray(t) ? t.forEach(a) : a(t), s;
  }
  clear(t) {
    const n = Object.keys(this);
    let r = n.length, s = !1;
    for (; r--; ) {
      const a = n[r];
      (!t || Ze(this, this[a], a, t, !0)) && (delete this[a], s = !0);
    }
    return s;
  }
  normalize(t) {
    const n = this, r = {};
    return c.forEach(this, (s, a) => {
      const o = c.findKey(r, a);
      if (o) {
        n[o] = Fe(s), delete n[a];
        return;
      }
      const l = t ? Xr(a) : String(a).trim();
      l !== a && delete n[a], n[l] = Fe(s), r[l] = !0;
    }), this;
  }
  concat(...t) {
    return this.constructor.concat(this, ...t);
  }
  toJSON(t) {
    const n = /* @__PURE__ */ Object.create(null);
    return c.forEach(this, (r, s) => {
      r != null && r !== !1 && (n[s] = t && c.isArray(r) ? r.join(", ") : r);
    }), n;
  }
  [Symbol.iterator]() {
    return Object.entries(this.toJSON())[Symbol.iterator]();
  }
  toString() {
    return Object.entries(this.toJSON()).map(([t, n]) => t + ": " + n).join(`
`);
  }
  getSetCookie() {
    return this.get("set-cookie") || [];
  }
  get [Symbol.toStringTag]() {
    return "AxiosHeaders";
  }
  static from(t) {
    return t instanceof this ? t : new this(t);
  }
  static concat(t, ...n) {
    const r = new this(t);
    return n.forEach((s) => r.set(s)), r;
  }
  static accessor(t) {
    const r = (this[Nt] = this[Nt] = {
      accessors: {}
    }).accessors, s = this.prototype;
    function a(o) {
      const l = we(o);
      r[l] || (Gr(s, o), r[l] = !0);
    }
    return c.isArray(t) ? t.forEach(a) : a(t), this;
  }
};
q.accessor(["Content-Type", "Content-Length", "Accept", "Accept-Encoding", "User-Agent", "Authorization"]);
c.reduceDescriptors(q.prototype, ({ value: e }, t) => {
  let n = t[0].toUpperCase() + t.slice(1);
  return {
    get: () => e,
    set(r) {
      this[n] = r;
    }
  };
});
c.freezeMethods(q);
function Qe(e, t) {
  const n = this || xe, r = t || n, s = q.from(r.headers);
  let a = r.data;
  return c.forEach(e, function(l) {
    a = l.call(n, a, s.normalize(), t ? t.status : void 0);
  }), s.normalize(), a;
}
function an(e) {
  return !!(e && e.__CANCEL__);
}
function de(e, t, n) {
  x.call(this, e ?? "canceled", x.ERR_CANCELED, t, n), this.name = "CanceledError";
}
c.inherits(de, x, {
  __CANCEL__: !0
});
function cn(e, t, n) {
  const r = n.config.validateStatus;
  !n.status || !r || r(n.status) ? e(n) : t(new x(
    "Request failed with status code " + n.status,
    [x.ERR_BAD_REQUEST, x.ERR_BAD_RESPONSE][Math.floor(n.status / 100) - 4],
    n.config,
    n.request,
    n
  ));
}
function Zr(e) {
  const t = /^([-+\w]{1,25})(:?\/\/|:)/.exec(e);
  return t && t[1] || "";
}
function Qr(e, t) {
  e = e || 10;
  const n = new Array(e), r = new Array(e);
  let s = 0, a = 0, o;
  return t = t !== void 0 ? t : 1e3, function(m) {
    const h = Date.now(), u = r[a];
    o || (o = h), n[s] = m, r[s] = h;
    let y = a, E = 0;
    for (; y !== s; )
      E += n[y++], y = y % e;
    if (s = (s + 1) % e, s === a && (a = (a + 1) % e), h - o < t)
      return;
    const R = u && h - u;
    return R ? Math.round(E * 1e3 / R) : void 0;
  };
}
function es(e, t) {
  let n = 0, r = 1e3 / t, s, a;
  const o = (h, u = Date.now()) => {
    n = u, s = null, a && (clearTimeout(a), a = null), e(...h);
  };
  return [(...h) => {
    const u = Date.now(), y = u - n;
    y >= r ? o(h, u) : (s = h, a || (a = setTimeout(() => {
      a = null, o(s);
    }, r - y)));
  }, () => s && o(s)];
}
const Le = (e, t, n = 3) => {
  let r = 0;
  const s = Qr(50, 250);
  return es((a) => {
    const o = a.loaded, l = a.lengthComputable ? a.total : void 0, m = o - r, h = s(m), u = o <= l;
    r = o;
    const y = {
      loaded: o,
      total: l,
      progress: l ? o / l : void 0,
      bytes: m,
      rate: h || void 0,
      estimated: h && l && u ? (l - o) / h : void 0,
      event: a,
      lengthComputable: l != null,
      [t ? "download" : "upload"]: !0
    };
    e(y);
  }, n);
}, Pt = (e, t) => {
  const n = e != null;
  return [(r) => t[0]({
    lengthComputable: n,
    total: e,
    loaded: r
  }), t[1]];
}, kt = (e) => (...t) => c.asap(() => e(...t)), ts = D.hasStandardBrowserEnv ? /* @__PURE__ */ ((e, t) => (n) => (n = new URL(n, D.origin), e.protocol === n.protocol && e.host === n.host && (t || e.port === n.port)))(
  new URL(D.origin),
  D.navigator && /(msie|trident)/i.test(D.navigator.userAgent)
) : () => !0, ns = D.hasStandardBrowserEnv ? (
  // Standard browser envs support document.cookie
  {
    write(e, t, n, r, s, a, o) {
      if (typeof document > "u") return;
      const l = [`${e}=${encodeURIComponent(t)}`];
      c.isNumber(n) && l.push(`expires=${new Date(n).toUTCString()}`), c.isString(r) && l.push(`path=${r}`), c.isString(s) && l.push(`domain=${s}`), a === !0 && l.push("secure"), c.isString(o) && l.push(`SameSite=${o}`), document.cookie = l.join("; ");
    },
    read(e) {
      if (typeof document > "u") return null;
      const t = document.cookie.match(new RegExp("(?:^|; )" + e + "=([^;]*)"));
      return t ? decodeURIComponent(t[1]) : null;
    },
    remove(e) {
      this.write(e, "", Date.now() - 864e5, "/");
    }
  }
) : (
  // Non-standard browser env (web workers, react-native) lack needed support.
  {
    write() {
    },
    read() {
      return null;
    },
    remove() {
    }
  }
);
function rs(e) {
  return /^([a-z][a-z\d+\-.]*:)?\/\//i.test(e);
}
function ss(e, t) {
  return t ? e.replace(/\/?\/$/, "") + "/" + t.replace(/^\/+/, "") : e;
}
function ln(e, t, n) {
  let r = !rs(t);
  return e && (r || n == !1) ? ss(e, t) : t;
}
const Ft = (e) => e instanceof q ? { ...e } : e;
function ie(e, t) {
  t = t || {};
  const n = {};
  function r(h, u, y, E) {
    return c.isPlainObject(h) && c.isPlainObject(u) ? c.merge.call({ caseless: E }, h, u) : c.isPlainObject(u) ? c.merge({}, u) : c.isArray(u) ? u.slice() : u;
  }
  function s(h, u, y, E) {
    if (c.isUndefined(u)) {
      if (!c.isUndefined(h))
        return r(void 0, h, y, E);
    } else return r(h, u, y, E);
  }
  function a(h, u) {
    if (!c.isUndefined(u))
      return r(void 0, u);
  }
  function o(h, u) {
    if (c.isUndefined(u)) {
      if (!c.isUndefined(h))
        return r(void 0, h);
    } else return r(void 0, u);
  }
  function l(h, u, y) {
    if (y in t)
      return r(h, u);
    if (y in e)
      return r(void 0, h);
  }
  const m = {
    url: a,
    method: a,
    data: a,
    baseURL: o,
    transformRequest: o,
    transformResponse: o,
    paramsSerializer: o,
    timeout: o,
    timeoutMessage: o,
    withCredentials: o,
    withXSRFToken: o,
    adapter: o,
    responseType: o,
    xsrfCookieName: o,
    xsrfHeaderName: o,
    onUploadProgress: o,
    onDownloadProgress: o,
    decompress: o,
    maxContentLength: o,
    maxBodyLength: o,
    beforeRedirect: o,
    transport: o,
    httpAgent: o,
    httpsAgent: o,
    cancelToken: o,
    socketPath: o,
    responseEncoding: o,
    validateStatus: l,
    headers: (h, u, y) => s(Ft(h), Ft(u), y, !0)
  };
  return c.forEach(Object.keys({ ...e, ...t }), function(u) {
    const y = m[u] || s, E = y(e[u], t[u], u);
    c.isUndefined(E) && y !== l || (n[u] = E);
  }), n;
}
const un = (e) => {
  const t = ie({}, e);
  let { data: n, withXSRFToken: r, xsrfHeaderName: s, xsrfCookieName: a, headers: o, auth: l } = t;
  if (t.headers = o = q.from(o), t.url = rn(ln(t.baseURL, t.url, t.allowAbsoluteUrls), e.params, e.paramsSerializer), l && o.set(
    "Authorization",
    "Basic " + btoa((l.username || "") + ":" + (l.password ? unescape(encodeURIComponent(l.password)) : ""))
  ), c.isFormData(n)) {
    if (D.hasStandardBrowserEnv || D.hasStandardBrowserWebWorkerEnv)
      o.setContentType(void 0);
    else if (c.isFunction(n.getHeaders)) {
      const m = n.getHeaders(), h = ["content-type", "content-length"];
      Object.entries(m).forEach(([u, y]) => {
        h.includes(u.toLowerCase()) && o.set(u, y);
      });
    }
  }
  if (D.hasStandardBrowserEnv && (r && c.isFunction(r) && (r = r(t)), r || r !== !1 && ts(t.url))) {
    const m = s && a && ns.read(a);
    m && o.set(s, m);
  }
  return t;
}, is = typeof XMLHttpRequest < "u", os = is && function(e) {
  return new Promise(function(n, r) {
    const s = un(e);
    let a = s.data;
    const o = q.from(s.headers).normalize();
    let { responseType: l, onUploadProgress: m, onDownloadProgress: h } = s, u, y, E, R, f;
    function w() {
      R && R(), f && f(), s.cancelToken && s.cancelToken.unsubscribe(u), s.signal && s.signal.removeEventListener("abort", u);
    }
    let b = new XMLHttpRequest();
    b.open(s.method.toUpperCase(), s.url, !0), b.timeout = s.timeout;
    function j() {
      if (!b)
        return;
      const P = q.from(
        "getAllResponseHeaders" in b && b.getAllResponseHeaders()
      ), H = {
        data: !l || l === "text" || l === "json" ? b.responseText : b.response,
        status: b.status,
        statusText: b.statusText,
        headers: P,
        config: e,
        request: b
      };
      cn(function(I) {
        n(I), w();
      }, function(I) {
        r(I), w();
      }, H), b = null;
    }
    "onloadend" in b ? b.onloadend = j : b.onreadystatechange = function() {
      !b || b.readyState !== 4 || b.status === 0 && !(b.responseURL && b.responseURL.indexOf("file:") === 0) || setTimeout(j);
    }, b.onabort = function() {
      b && (r(new x("Request aborted", x.ECONNABORTED, e, b)), b = null);
    }, b.onerror = function(F) {
      const H = F && F.message ? F.message : "Network Error", X = new x(H, x.ERR_NETWORK, e, b);
      X.event = F || null, r(X), b = null;
    }, b.ontimeout = function() {
      let F = s.timeout ? "timeout of " + s.timeout + "ms exceeded" : "timeout exceeded";
      const H = s.transitional || sn;
      s.timeoutErrorMessage && (F = s.timeoutErrorMessage), r(new x(
        F,
        H.clarifyTimeoutError ? x.ETIMEDOUT : x.ECONNABORTED,
        e,
        b
      )), b = null;
    }, a === void 0 && o.setContentType(null), "setRequestHeader" in b && c.forEach(o.toJSON(), function(F, H) {
      b.setRequestHeader(H, F);
    }), c.isUndefined(s.withCredentials) || (b.withCredentials = !!s.withCredentials), l && l !== "json" && (b.responseType = s.responseType), h && ([E, f] = Le(h, !0), b.addEventListener("progress", E)), m && b.upload && ([y, R] = Le(m), b.upload.addEventListener("progress", y), b.upload.addEventListener("loadend", R)), (s.cancelToken || s.signal) && (u = (P) => {
      b && (r(!P || P.type ? new de(null, e, b) : P), b.abort(), b = null);
    }, s.cancelToken && s.cancelToken.subscribe(u), s.signal && (s.signal.aborted ? u() : s.signal.addEventListener("abort", u)));
    const _ = Zr(s.url);
    if (_ && D.protocols.indexOf(_) === -1) {
      r(new x("Unsupported protocol " + _ + ":", x.ERR_BAD_REQUEST, e));
      return;
    }
    b.send(a || null);
  });
}, as = (e, t) => {
  const { length: n } = e = e ? e.filter(Boolean) : [];
  if (t || n) {
    let r = new AbortController(), s;
    const a = function(h) {
      if (!s) {
        s = !0, l();
        const u = h instanceof Error ? h : this.reason;
        r.abort(u instanceof x ? u : new de(u instanceof Error ? u.message : u));
      }
    };
    let o = t && setTimeout(() => {
      o = null, a(new x(`timeout ${t} of ms exceeded`, x.ETIMEDOUT));
    }, t);
    const l = () => {
      e && (o && clearTimeout(o), o = null, e.forEach((h) => {
        h.unsubscribe ? h.unsubscribe(a) : h.removeEventListener("abort", a);
      }), e = null);
    };
    e.forEach((h) => h.addEventListener("abort", a));
    const { signal: m } = r;
    return m.unsubscribe = () => c.asap(l), m;
  }
}, cs = function* (e, t) {
  let n = e.byteLength;
  if (n < t) {
    yield e;
    return;
  }
  let r = 0, s;
  for (; r < n; )
    s = r + t, yield e.slice(r, s), r = s;
}, ls = async function* (e, t) {
  for await (const n of us(e))
    yield* cs(n, t);
}, us = async function* (e) {
  if (e[Symbol.asyncIterator]) {
    yield* e;
    return;
  }
  const t = e.getReader();
  try {
    for (; ; ) {
      const { done: n, value: r } = await t.read();
      if (n)
        break;
      yield r;
    }
  } finally {
    await t.cancel();
  }
}, Dt = (e, t, n, r) => {
  const s = ls(e, t);
  let a = 0, o, l = (m) => {
    o || (o = !0, r && r(m));
  };
  return new ReadableStream({
    async pull(m) {
      try {
        const { done: h, value: u } = await s.next();
        if (h) {
          l(), m.close();
          return;
        }
        let y = u.byteLength;
        if (n) {
          let E = a += y;
          n(E);
        }
        m.enqueue(new Uint8Array(u));
      } catch (h) {
        throw l(h), h;
      }
    },
    cancel(m) {
      return l(m), s.return();
    }
  }, {
    highWaterMark: 2
  });
}, Ut = 64 * 1024, { isFunction: Pe } = c, fs = (({ Request: e, Response: t }) => ({
  Request: e,
  Response: t
}))(c.global), {
  ReadableStream: Lt,
  TextEncoder: It
} = c.global, $t = (e, ...t) => {
  try {
    return !!e(...t);
  } catch {
    return !1;
  }
}, ds = (e) => {
  e = c.merge.call({
    skipUndefined: !0
  }, fs, e);
  const { fetch: t, Request: n, Response: r } = e, s = t ? Pe(t) : typeof fetch == "function", a = Pe(n), o = Pe(r);
  if (!s)
    return !1;
  const l = s && Pe(Lt), m = s && (typeof It == "function" ? /* @__PURE__ */ ((f) => (w) => f.encode(w))(new It()) : async (f) => new Uint8Array(await new n(f).arrayBuffer())), h = a && l && $t(() => {
    let f = !1;
    const w = new n(D.origin, {
      body: new Lt(),
      method: "POST",
      get duplex() {
        return f = !0, "half";
      }
    }).headers.has("Content-Type");
    return f && !w;
  }), u = o && l && $t(() => c.isReadableStream(new r("").body)), y = {
    stream: u && ((f) => f.body)
  };
  s && ["text", "arrayBuffer", "blob", "formData", "stream"].forEach((f) => {
    !y[f] && (y[f] = (w, b) => {
      let j = w && w[f];
      if (j)
        return j.call(w);
      throw new x(`Response type '${f}' is not supported`, x.ERR_NOT_SUPPORT, b);
    });
  });
  const E = async (f) => {
    if (f == null)
      return 0;
    if (c.isBlob(f))
      return f.size;
    if (c.isSpecCompliantForm(f))
      return (await new n(D.origin, {
        method: "POST",
        body: f
      }).arrayBuffer()).byteLength;
    if (c.isArrayBufferView(f) || c.isArrayBuffer(f))
      return f.byteLength;
    if (c.isURLSearchParams(f) && (f = f + ""), c.isString(f))
      return (await m(f)).byteLength;
  }, R = async (f, w) => {
    const b = c.toFiniteNumber(f.getContentLength());
    return b ?? E(w);
  };
  return async (f) => {
    let {
      url: w,
      method: b,
      data: j,
      signal: _,
      cancelToken: P,
      timeout: F,
      onDownloadProgress: H,
      onUploadProgress: X,
      responseType: I,
      headers: he,
      withCredentials: Q = "same-origin",
      fetchOptions: Se
    } = un(f), Oe = t || fetch;
    I = I ? (I + "").toLowerCase() : "text";
    let ee = as([_, P && P.toAbortSignal()], F), $ = null;
    const U = ee && ee.unsubscribe && (() => {
      ee.unsubscribe();
    });
    let Z;
    try {
      if (X && h && b !== "get" && b !== "head" && (Z = await R(he, j)) !== 0) {
        let J = new n(w, {
          method: "POST",
          body: j,
          duplex: "half"
        }), G;
        if (c.isFormData(j) && (G = J.headers.get("content-type")) && he.setContentType(G), J.body) {
          const [oe, ae] = Pt(
            Z,
            Le(kt(X))
          );
          j = Dt(J.body, Ut, oe, ae);
        }
      }
      c.isString(Q) || (Q = Q ? "include" : "omit");
      const W = a && "credentials" in n.prototype, pe = {
        ...Se,
        signal: ee,
        method: b.toUpperCase(),
        headers: he.normalize().toJSON(),
        body: j,
        duplex: "half",
        credentials: W ? Q : void 0
      };
      $ = a && new n(w, pe);
      let V = await (a ? Oe($, Se) : Oe(w, pe));
      const me = u && (I === "stream" || I === "response");
      if (u && (H || me && U)) {
        const J = {};
        ["status", "statusText", "headers"].forEach((je) => {
          J[je] = V[je];
        });
        const G = c.toFiniteNumber(V.headers.get("content-length")), [oe, ae] = H && Pt(
          G,
          Le(kt(H), !0)
        ) || [];
        V = new r(
          Dt(V.body, Ut, oe, () => {
            ae && ae(), U && U();
          }),
          J
        );
      }
      I = I || "text";
      let Te = await y[c.findKey(y, I) || "text"](V, f);
      return !me && U && U(), await new Promise((J, G) => {
        cn(J, G, {
          data: Te,
          headers: q.from(V.headers),
          status: V.status,
          statusText: V.statusText,
          config: f,
          request: $
        });
      });
    } catch (W) {
      throw U && U(), W && W.name === "TypeError" && /Load failed|fetch/i.test(W.message) ? Object.assign(
        new x("Network Error", x.ERR_NETWORK, f, $),
        {
          cause: W.cause || W
        }
      ) : x.from(W, W && W.code, f, $);
    }
  };
}, hs = /* @__PURE__ */ new Map(), fn = (e) => {
  let t = e && e.env || {};
  const { fetch: n, Request: r, Response: s } = t, a = [
    r,
    s,
    n
  ];
  let o = a.length, l = o, m, h, u = hs;
  for (; l--; )
    m = a[l], h = u.get(m), h === void 0 && u.set(m, h = l ? /* @__PURE__ */ new Map() : ds(t)), u = h;
  return h;
};
fn();
const lt = {
  http: Ar,
  xhr: os,
  fetch: {
    get: fn
  }
};
c.forEach(lt, (e, t) => {
  if (e) {
    try {
      Object.defineProperty(e, "name", { value: t });
    } catch {
    }
    Object.defineProperty(e, "adapterName", { value: t });
  }
});
const Bt = (e) => `- ${e}`, ps = (e) => c.isFunction(e) || e === null || e === !1;
function ms(e, t) {
  e = c.isArray(e) ? e : [e];
  const { length: n } = e;
  let r, s;
  const a = {};
  for (let o = 0; o < n; o++) {
    r = e[o];
    let l;
    if (s = r, !ps(r) && (s = lt[(l = String(r)).toLowerCase()], s === void 0))
      throw new x(`Unknown adapter '${l}'`);
    if (s && (c.isFunction(s) || (s = s.get(t))))
      break;
    a[l || "#" + o] = s;
  }
  if (!s) {
    const o = Object.entries(a).map(
      ([m, h]) => `adapter ${m} ` + (h === !1 ? "is not supported by the environment" : "is not available in the build")
    );
    let l = n ? o.length > 1 ? `since :
` + o.map(Bt).join(`
`) : " " + Bt(o[0]) : "as no adapter specified";
    throw new x(
      "There is no suitable adapter to dispatch the request " + l,
      "ERR_NOT_SUPPORT"
    );
  }
  return s;
}
const dn = {
  /**
   * Resolve an adapter from a list of adapter names or functions.
   * @type {Function}
   */
  getAdapter: ms,
  /**
   * Exposes all known adapters
   * @type {Object<string, Function|Object>}
   */
  adapters: lt
};
function et(e) {
  if (e.cancelToken && e.cancelToken.throwIfRequested(), e.signal && e.signal.aborted)
    throw new de(null, e);
}
function Mt(e) {
  return et(e), e.headers = q.from(e.headers), e.data = Qe.call(
    e,
    e.transformRequest
  ), ["post", "put", "patch"].indexOf(e.method) !== -1 && e.headers.setContentType("application/x-www-form-urlencoded", !1), dn.getAdapter(e.adapter || xe.adapter, e)(e).then(function(r) {
    return et(e), r.data = Qe.call(
      e,
      e.transformResponse,
      r
    ), r.headers = q.from(r.headers), r;
  }, function(r) {
    return an(r) || (et(e), r && r.response && (r.response.data = Qe.call(
      e,
      e.transformResponse,
      r.response
    ), r.response.headers = q.from(r.response.headers))), Promise.reject(r);
  });
}
const hn = "1.13.2", qe = {};
["object", "boolean", "number", "function", "string", "symbol"].forEach((e, t) => {
  qe[e] = function(r) {
    return typeof r === e || "a" + (t < 1 ? "n " : " ") + e;
  };
});
const qt = {};
qe.transitional = function(t, n, r) {
  function s(a, o) {
    return "[Axios v" + hn + "] Transitional option '" + a + "'" + o + (r ? ". " + r : "");
  }
  return (a, o, l) => {
    if (t === !1)
      throw new x(
        s(o, " has been removed" + (n ? " in " + n : "")),
        x.ERR_DEPRECATED
      );
    return n && !qt[o] && (qt[o] = !0, console.warn(
      s(
        o,
        " has been deprecated since v" + n + " and will be removed in the near future"
      )
    )), t ? t(a, o, l) : !0;
  };
};
qe.spelling = function(t) {
  return (n, r) => (console.warn(`${r} is likely a misspelling of ${t}`), !0);
};
function ys(e, t, n) {
  if (typeof e != "object")
    throw new x("options must be an object", x.ERR_BAD_OPTION_VALUE);
  const r = Object.keys(e);
  let s = r.length;
  for (; s-- > 0; ) {
    const a = r[s], o = t[a];
    if (o) {
      const l = e[a], m = l === void 0 || o(l, a, e);
      if (m !== !0)
        throw new x("option " + a + " must be " + m, x.ERR_BAD_OPTION_VALUE);
      continue;
    }
    if (n !== !0)
      throw new x("Unknown option " + a, x.ERR_BAD_OPTION);
  }
}
const De = {
  assertOptions: ys,
  validators: qe
}, Y = De.validators;
let se = class {
  constructor(t) {
    this.defaults = t || {}, this.interceptors = {
      request: new At(),
      response: new At()
    };
  }
  /**
   * Dispatch a request
   *
   * @param {String|Object} configOrUrl The config specific for this request (merged with this.defaults)
   * @param {?Object} config
   *
   * @returns {Promise} The Promise to be fulfilled
   */
  async request(t, n) {
    try {
      return await this._request(t, n);
    } catch (r) {
      if (r instanceof Error) {
        let s = {};
        Error.captureStackTrace ? Error.captureStackTrace(s) : s = new Error();
        const a = s.stack ? s.stack.replace(/^.+\n/, "") : "";
        try {
          r.stack ? a && !String(r.stack).endsWith(a.replace(/^.+\n.+\n/, "")) && (r.stack += `
` + a) : r.stack = a;
        } catch {
        }
      }
      throw r;
    }
  }
  _request(t, n) {
    typeof t == "string" ? (n = n || {}, n.url = t) : n = t || {}, n = ie(this.defaults, n);
    const { transitional: r, paramsSerializer: s, headers: a } = n;
    r !== void 0 && De.assertOptions(r, {
      silentJSONParsing: Y.transitional(Y.boolean),
      forcedJSONParsing: Y.transitional(Y.boolean),
      clarifyTimeoutError: Y.transitional(Y.boolean)
    }, !1), s != null && (c.isFunction(s) ? n.paramsSerializer = {
      serialize: s
    } : De.assertOptions(s, {
      encode: Y.function,
      serialize: Y.function
    }, !0)), n.allowAbsoluteUrls !== void 0 || (this.defaults.allowAbsoluteUrls !== void 0 ? n.allowAbsoluteUrls = this.defaults.allowAbsoluteUrls : n.allowAbsoluteUrls = !0), De.assertOptions(n, {
      baseUrl: Y.spelling("baseURL"),
      withXsrfToken: Y.spelling("withXSRFToken")
    }, !0), n.method = (n.method || this.defaults.method || "get").toLowerCase();
    let o = a && c.merge(
      a.common,
      a[n.method]
    );
    a && c.forEach(
      ["delete", "get", "head", "post", "put", "patch", "common"],
      (f) => {
        delete a[f];
      }
    ), n.headers = q.concat(o, a);
    const l = [];
    let m = !0;
    this.interceptors.request.forEach(function(w) {
      typeof w.runWhen == "function" && w.runWhen(n) === !1 || (m = m && w.synchronous, l.unshift(w.fulfilled, w.rejected));
    });
    const h = [];
    this.interceptors.response.forEach(function(w) {
      h.push(w.fulfilled, w.rejected);
    });
    let u, y = 0, E;
    if (!m) {
      const f = [Mt.bind(this), void 0];
      for (f.unshift(...l), f.push(...h), E = f.length, u = Promise.resolve(n); y < E; )
        u = u.then(f[y++], f[y++]);
      return u;
    }
    E = l.length;
    let R = n;
    for (; y < E; ) {
      const f = l[y++], w = l[y++];
      try {
        R = f(R);
      } catch (b) {
        w.call(this, b);
        break;
      }
    }
    try {
      u = Mt.call(this, R);
    } catch (f) {
      return Promise.reject(f);
    }
    for (y = 0, E = h.length; y < E; )
      u = u.then(h[y++], h[y++]);
    return u;
  }
  getUri(t) {
    t = ie(this.defaults, t);
    const n = ln(t.baseURL, t.url, t.allowAbsoluteUrls);
    return rn(n, t.params, t.paramsSerializer);
  }
};
c.forEach(["delete", "get", "head", "options"], function(t) {
  se.prototype[t] = function(n, r) {
    return this.request(ie(r || {}, {
      method: t,
      url: n,
      data: (r || {}).data
    }));
  };
});
c.forEach(["post", "put", "patch"], function(t) {
  function n(r) {
    return function(a, o, l) {
      return this.request(ie(l || {}, {
        method: t,
        headers: r ? {
          "Content-Type": "multipart/form-data"
        } : {},
        url: a,
        data: o
      }));
    };
  }
  se.prototype[t] = n(), se.prototype[t + "Form"] = n(!0);
});
let gs = class pn {
  constructor(t) {
    if (typeof t != "function")
      throw new TypeError("executor must be a function.");
    let n;
    this.promise = new Promise(function(a) {
      n = a;
    });
    const r = this;
    this.promise.then((s) => {
      if (!r._listeners) return;
      let a = r._listeners.length;
      for (; a-- > 0; )
        r._listeners[a](s);
      r._listeners = null;
    }), this.promise.then = (s) => {
      let a;
      const o = new Promise((l) => {
        r.subscribe(l), a = l;
      }).then(s);
      return o.cancel = function() {
        r.unsubscribe(a);
      }, o;
    }, t(function(a, o, l) {
      r.reason || (r.reason = new de(a, o, l), n(r.reason));
    });
  }
  /**
   * Throws a `CanceledError` if cancellation has been requested.
   */
  throwIfRequested() {
    if (this.reason)
      throw this.reason;
  }
  /**
   * Subscribe to the cancel signal
   */
  subscribe(t) {
    if (this.reason) {
      t(this.reason);
      return;
    }
    this._listeners ? this._listeners.push(t) : this._listeners = [t];
  }
  /**
   * Unsubscribe from the cancel signal
   */
  unsubscribe(t) {
    if (!this._listeners)
      return;
    const n = this._listeners.indexOf(t);
    n !== -1 && this._listeners.splice(n, 1);
  }
  toAbortSignal() {
    const t = new AbortController(), n = (r) => {
      t.abort(r);
    };
    return this.subscribe(n), t.signal.unsubscribe = () => this.unsubscribe(n), t.signal;
  }
  /**
   * Returns an object that contains a new `CancelToken` and a function that, when called,
   * cancels the `CancelToken`.
   */
  static source() {
    let t;
    return {
      token: new pn(function(s) {
        t = s;
      }),
      cancel: t
    };
  }
};
function bs(e) {
  return function(n) {
    return e.apply(null, n);
  };
}
function ws(e) {
  return c.isObject(e) && e.isAxiosError === !0;
}
const it = {
  Continue: 100,
  SwitchingProtocols: 101,
  Processing: 102,
  EarlyHints: 103,
  Ok: 200,
  Created: 201,
  Accepted: 202,
  NonAuthoritativeInformation: 203,
  NoContent: 204,
  ResetContent: 205,
  PartialContent: 206,
  MultiStatus: 207,
  AlreadyReported: 208,
  ImUsed: 226,
  MultipleChoices: 300,
  MovedPermanently: 301,
  Found: 302,
  SeeOther: 303,
  NotModified: 304,
  UseProxy: 305,
  Unused: 306,
  TemporaryRedirect: 307,
  PermanentRedirect: 308,
  BadRequest: 400,
  Unauthorized: 401,
  PaymentRequired: 402,
  Forbidden: 403,
  NotFound: 404,
  MethodNotAllowed: 405,
  NotAcceptable: 406,
  ProxyAuthenticationRequired: 407,
  RequestTimeout: 408,
  Conflict: 409,
  Gone: 410,
  LengthRequired: 411,
  PreconditionFailed: 412,
  PayloadTooLarge: 413,
  UriTooLong: 414,
  UnsupportedMediaType: 415,
  RangeNotSatisfiable: 416,
  ExpectationFailed: 417,
  ImATeapot: 418,
  MisdirectedRequest: 421,
  UnprocessableEntity: 422,
  Locked: 423,
  FailedDependency: 424,
  TooEarly: 425,
  UpgradeRequired: 426,
  PreconditionRequired: 428,
  TooManyRequests: 429,
  RequestHeaderFieldsTooLarge: 431,
  UnavailableForLegalReasons: 451,
  InternalServerError: 500,
  NotImplemented: 501,
  BadGateway: 502,
  ServiceUnavailable: 503,
  GatewayTimeout: 504,
  HttpVersionNotSupported: 505,
  VariantAlsoNegotiates: 506,
  InsufficientStorage: 507,
  LoopDetected: 508,
  NotExtended: 510,
  NetworkAuthenticationRequired: 511,
  WebServerIsDown: 521,
  ConnectionTimedOut: 522,
  OriginIsUnreachable: 523,
  TimeoutOccurred: 524,
  SslHandshakeFailed: 525,
  InvalidSslCertificate: 526
};
Object.entries(it).forEach(([e, t]) => {
  it[t] = e;
});
function mn(e) {
  const t = new se(e), n = zt(se.prototype.request, t);
  return c.extend(n, se.prototype, t, { allOwnKeys: !0 }), c.extend(n, t, null, { allOwnKeys: !0 }), n.create = function(s) {
    return mn(ie(e, s));
  }, n;
}
const A = mn(xe);
A.Axios = se;
A.CanceledError = de;
A.CancelToken = gs;
A.isCancel = an;
A.VERSION = hn;
A.toFormData = Me;
A.AxiosError = x;
A.Cancel = A.CanceledError;
A.all = function(t) {
  return Promise.all(t);
};
A.spread = bs;
A.isAxiosError = ws;
A.mergeConfig = ie;
A.AxiosHeaders = q;
A.formToJSON = (e) => on(c.isHTMLForm(e) ? new FormData(e) : e);
A.getAdapter = dn.getAdapter;
A.HttpStatusCode = it;
A.default = A;
const {
  Axios: Us,
  AxiosError: Ls,
  CanceledError: Is,
  isCancel: $s,
  CancelToken: Bs,
  VERSION: Ms,
  all: qs,
  Cancel: Hs,
  isAxiosError: Ws,
  spread: zs,
  toFormData: Vs,
  AxiosHeaders: Js,
  HttpStatusCode: Ks,
  formToJSON: Ys,
  getAdapter: Xs,
  mergeConfig: Gs
} = A;
class vs {
  constructor(t = "http://localhost:8000/api/v1") {
    Ge(this, "client");
    Ge(this, "baseUrl");
    this.baseUrl = t, this.client = A.create({
      baseURL: t,
      timeout: 1e4,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      }
    });
  }
  /**
   * Get epistemic context for a specific commit
   */
  async getCommitEpistemic(t) {
    try {
      return (await this.client.get(
        `/commits/${t}/epistemic`
      )).data;
    } catch (n) {
      throw this.handleError(n, `Failed to fetch commit epistemic: ${t}`), n;
    }
  }
  /**
   * Get learning deltas for a session
   */
  async getSessionDeltas(t) {
    try {
      return (await this.client.get(
        `/sessions/${t}/deltas`
      )).data;
    } catch (n) {
      throw this.handleError(n, `Failed to fetch session deltas: ${t}`), n;
    }
  }
  /**
   * Verify signature of a checkpoint
   */
  async verifyCheckpoint(t, n, r, s) {
    try {
      const a = s ? { public_key: s } : {};
      return (await this.client.get(
        `/checkpoints/${t}/${n}/${r}/verify`,
        { params: a }
      )).data;
    } catch (a) {
      throw this.handleError(
        a,
        `Failed to verify checkpoint: ${t}/${n}/${r}`
      ), a;
    }
  }
  /**
   * Get file uncertainty/confidence metrics
   */
  async getFileUncertainty(t) {
    try {
      return (await this.client.get(
        `/files/${encodeURIComponent(t)}/uncertainty`
      )).data;
    } catch (n) {
      throw this.handleError(n, `Failed to fetch file uncertainty: ${t}`), n;
    }
  }
  /**
   * Get AI learning curve over time
   */
  async getAILearningCurve(t, n, r) {
    try {
      const s = {};
      return n && (s.since = n), r && (s.limit = r), (await this.client.get(
        `/ai/${t}/learning-curve`,
        { params: s }
      )).data;
    } catch (s) {
      throw this.handleError(s, `Failed to fetch AI learning curve: ${t}`), s;
    }
  }
  /**
   * Compare learning curves across multiple AIs
   */
  async compareAIs(t, n, r) {
    try {
      const s = {
        ai_ids: t.join(",")
      };
      return n && (s.since = n), r && (s.metric = r), (await this.client.get("/compare-ais", { params: s })).data;
    } catch (s) {
      throw this.handleError(s, `Failed to compare AIs: ${t.join(", ")}`), s;
    }
  }
  /**
   * Health check - verify API is available
   */
  async healthCheck() {
    try {
      return (await A.get(`${this.baseUrl.replace("/api/v1", "")}/health`)).status === 200;
    } catch (t) {
      return console.warn("Dashboard API health check failed", t), !1;
    }
  }
  /**
   * Get API base URL
   */
  getBaseUrl() {
    return this.baseUrl;
  }
  /**
   * Handle API errors with logging
   */
  handleError(t, n) {
    var r, s, a;
    A.isAxiosError(t) ? console.error(n, {
      status: (r = t.response) == null ? void 0 : r.status,
      statusText: (s = t.response) == null ? void 0 : s.statusText,
      data: (a = t.response) == null ? void 0 : a.data
    }) : console.error(n, t);
  }
}
const Ue = new vs(), Es = ({
  score: e,
  label: t = "Confidence",
  subtitle: n,
  size: r = "medium"
}) => {
  const s = Math.round(e * 100), a = Rs(e), o = xs(e);
  return /* @__PURE__ */ d.jsxs("div", { className: `confidence-badge ${r} ${a}`, children: [
    /* @__PURE__ */ d.jsxs("div", { className: "badge-content", children: [
      /* @__PURE__ */ d.jsxs("div", { className: "badge-percentage", style: { color: o }, children: [
        s,
        "%"
      ] }),
      /* @__PURE__ */ d.jsx("div", { className: "badge-label", children: t }),
      n && /* @__PURE__ */ d.jsx("div", { className: "badge-subtitle", children: n })
    ] }),
    /* @__PURE__ */ d.jsx("div", { className: "badge-indicator", style: { backgroundColor: o } })
  ] });
};
function Rs(e) {
  return e >= 0.9 ? "high" : e >= 0.7 ? "moderate" : e >= 0.5 ? "low" : "none";
}
function xs(e) {
  return e >= 0.9 ? "#22c55e" : e >= 0.7 ? "#eab308" : e >= 0.5 ? "#f97316" : "#ef4444";
}
const Ss = ({
  know: e,
  do: t,
  overall: n,
  context: r,
  clarity: s
}) => {
  const a = [
    { label: "KNOW", value: e, emoji: "📚" },
    { label: "DO", value: t, emoji: "⚙️" },
    ...r !== void 0 ? [{ label: "CONTEXT", value: r, emoji: "🗺️" }] : [],
    ...s !== void 0 ? [{ label: "CLARITY", value: s, emoji: "✨" }] : []
  ];
  return /* @__PURE__ */ d.jsxs("div", { className: "learning-delta", children: [
    /* @__PURE__ */ d.jsx("h3", { className: "delta-title", children: "📈 Learning Progress" }),
    /* @__PURE__ */ d.jsx("div", { className: "overall-delta", children: /* @__PURE__ */ d.jsxs("div", { className: "delta-metric", children: [
      /* @__PURE__ */ d.jsx("span", { className: "metric-label", children: "Overall Learning" }),
      /* @__PURE__ */ d.jsx("div", { className: "metric-bar", children: /* @__PURE__ */ d.jsx(
        "div",
        {
          className: "metric-fill positive",
          style: { width: `${Math.min(n * 100, 100)}%` }
        }
      ) }),
      /* @__PURE__ */ d.jsxs("span", { className: "metric-value", children: [
        "+",
        (n * 100).toFixed(0),
        "%"
      ] })
    ] }) }),
    /* @__PURE__ */ d.jsx("div", { className: "delta-breakdown", children: a.map((o) => /* @__PURE__ */ d.jsxs("div", { className: "delta-item", children: [
      /* @__PURE__ */ d.jsxs("div", { className: "delta-header", children: [
        /* @__PURE__ */ d.jsx("span", { className: "delta-emoji", children: o.emoji }),
        /* @__PURE__ */ d.jsx("span", { className: "delta-label", children: o.label }),
        /* @__PURE__ */ d.jsxs("span", { className: `delta-value ${o.value > 0 ? "positive" : "negative"}`, children: [
          o.value > 0 ? "+" : "",
          (o.value * 100).toFixed(0),
          "%"
        ] })
      ] }),
      /* @__PURE__ */ d.jsx("div", { className: "delta-bar", children: /* @__PURE__ */ d.jsx(
        "div",
        {
          className: `delta-bar-fill ${o.value > 0 ? "positive" : "negative"}`,
          style: {
            width: `${Math.abs(o.value) * 100}%`
          }
        }
      ) })
    ] }, o.label)) }),
    /* @__PURE__ */ d.jsx("div", { className: "delta-interpretation", children: /* @__PURE__ */ d.jsxs("p", { className: "interpretation-text", children: [
      n > 0.2 && /* @__PURE__ */ d.jsxs(d.Fragment, { children: [
        "✅ ",
        /* @__PURE__ */ d.jsx("strong", { children: "Significant learning" }),
        " occurred during this session. The AI developed new understanding and capability."
      ] }),
      n > 0.1 && n <= 0.2 && /* @__PURE__ */ d.jsxs(d.Fragment, { children: [
        "✓ ",
        /* @__PURE__ */ d.jsx("strong", { children: "Moderate learning" }),
        " occurred. The AI gained some new confidence."
      ] }),
      n <= 0.1 && /* @__PURE__ */ d.jsxs(d.Fragment, { children: [
        "→ ",
        /* @__PURE__ */ d.jsx("strong", { children: "Minimal learning" }),
        " or refactoring work. The AI was mostly working within existing confidence bounds."
      ] })
    ] }) })
  ] });
}, Os = ({
  sessionId: e,
  aiId: t,
  verified: n = !1,
  timestamp: r = (/* @__PURE__ */ new Date()).toISOString(),
  phase: s = "POSTFLIGHT",
  round: a = 1,
  onVerified: o
}) => {
  const [l, m] = ne(n), [h, u] = ne(!n), [y, E] = ne(null);
  Wt(() => {
    n || R();
  }, [e, s, a]);
  const R = async () => {
    try {
      u(!0);
      const w = await Ue.verifyCheckpoint(
        e,
        s,
        a
      );
      m(w.signature_verified), w.public_key && E(w.public_key), o == null || o(w.signature_verified);
    } catch (w) {
      console.error("Verification failed:", w), m(!1);
    } finally {
      u(!1);
    }
  }, f = (w) => {
    try {
      return new Date(w).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    } catch {
      return w;
    }
  };
  return h ? /* @__PURE__ */ d.jsxs("div", { className: "verification-badge checking", children: [
    /* @__PURE__ */ d.jsx("span", { className: "verification-icon", children: "⏳" }),
    /* @__PURE__ */ d.jsx("span", { className: "verification-text", children: "Verifying..." })
  ] }) : /* @__PURE__ */ d.jsxs("div", { className: `verification-badge ${l ? "verified" : "unverified"}`, children: [
    /* @__PURE__ */ d.jsxs("div", { className: "verification-content", children: [
      /* @__PURE__ */ d.jsx("span", { className: "verification-icon", children: l ? "✅" : "❌" }),
      /* @__PURE__ */ d.jsxs("div", { className: "verification-details", children: [
        /* @__PURE__ */ d.jsx("div", { className: "verification-status", children: l ? "Verified" : "Not Verified" }),
        /* @__PURE__ */ d.jsxs("div", { className: "verification-info", children: [
          /* @__PURE__ */ d.jsxs("span", { className: "info-ai", children: [
            "by ",
            t
          ] }),
          /* @__PURE__ */ d.jsx("span", { className: "info-date", children: f(r) })
        ] })
      ] })
    ] }),
    y && l && /* @__PURE__ */ d.jsxs("div", { className: "verification-details-tooltip", children: [
      /* @__PURE__ */ d.jsxs("p", { className: "small-text", children: [
        /* @__PURE__ */ d.jsx("strong", { children: "Ed25519 Public Key:" }),
        /* @__PURE__ */ d.jsx("br", {}),
        /* @__PURE__ */ d.jsx("code", { children: y })
      ] }),
      /* @__PURE__ */ d.jsx("p", { className: "small-text", children: "This commit's epistemic analysis was cryptographically signed by the listed AI system and can be independently verified." })
    ] }),
    !l && /* @__PURE__ */ d.jsx(
      "button",
      {
        className: "retry-verify",
        onClick: R,
        title: "Retry verification",
        children: "🔄"
      }
    )
  ] });
}, Zs = ({
  commitSha: e,
  onError: t
}) => {
  const [n, r] = ne(null), [s, a] = ne([]), [o, l] = ne(!0), [m, h] = ne(null);
  Wt(() => {
    u();
  }, [e]);
  const u = async () => {
    try {
      if (l(!0), h(null), !await Ue.healthCheck()) {
        h("Dashboard API is not available. Make sure it's running at the configured URL.");
        return;
      }
      const f = await Ue.getCommitEpistemic(e);
      if (!f.ok) {
        h("No epistemic data available for this commit");
        return;
      }
      if (r(f), f.files_changed && f.files_changed.length > 0) {
        const w = [];
        for (const b of f.files_changed)
          try {
            const j = await Ue.getFileUncertainty(b);
            w.push({
              name: b,
              confidence: j.aggregate_confidence,
              status: Cs(b)
              // Would need more info in real impl
            });
          } catch {
            w.push({
              name: b,
              confidence: f.epistemic_context.know,
              status: "modified"
            });
          }
        a(w);
      }
    } catch (R) {
      const f = R instanceof Error ? R : new Error(String(R));
      h(f.message), t == null || t(f);
    } finally {
      l(!1);
    }
  };
  if (o)
    return /* @__PURE__ */ d.jsxs("div", { className: "commit-insight loading", children: [
      /* @__PURE__ */ d.jsx("div", { className: "spinner" }),
      /* @__PURE__ */ d.jsx("p", { children: "Loading epistemic analysis..." })
    ] });
  if (m)
    return /* @__PURE__ */ d.jsxs("div", { className: "commit-insight error", children: [
      /* @__PURE__ */ d.jsx("div", { className: "error-icon", children: "⚠️" }),
      /* @__PURE__ */ d.jsx("h3", { children: "Epistemic Data Unavailable" }),
      /* @__PURE__ */ d.jsx("p", { children: m }),
      /* @__PURE__ */ d.jsx("button", { onClick: u, className: "retry-button", children: "Retry" })
    ] });
  if (!n)
    return /* @__PURE__ */ d.jsxs("div", { className: "commit-insight no-data", children: [
      /* @__PURE__ */ d.jsx("p", { children: "No epistemic analysis available for this commit." }),
      /* @__PURE__ */ d.jsx("p", { className: "help-text", children: "This commit was made before epistemic tracking was enabled, or the AI system hasn't analyzed it yet." })
    ] });
  const y = n.epistemic_context, E = n.learning_delta;
  return /* @__PURE__ */ d.jsxs("div", { className: "commit-insight", children: [
    /* @__PURE__ */ d.jsx("h2", { className: "section-title", children: "📊 Epistemic Analysis" }),
    /* @__PURE__ */ d.jsxs("div", { className: "insight-header", children: [
      /* @__PURE__ */ d.jsx("div", { className: "confidence-section", children: /* @__PURE__ */ d.jsx(
        Es,
        {
          score: y.know,
          label: "Confidence",
          subtitle: `KNOW: ${(y.know * 100).toFixed(0)}% | DO: ${(E.do * 100).toFixed(0)}%`
        }
      ) }),
      /* @__PURE__ */ d.jsx("div", { className: "verification-section", children: /* @__PURE__ */ d.jsx(
        Os,
        {
          sessionId: y.session_id,
          aiId: y.ai_id,
          verified: !0,
          timestamp: "2025-12-02T14:00:00Z"
        }
      ) })
    ] }),
    E.overall > 0 && /* @__PURE__ */ d.jsx(
      Ss,
      {
        know: E.know,
        do: E.do,
        overall: E.overall
      }
    ),
    /* @__PURE__ */ d.jsxs("div", { className: "risk-assessment", children: [
      /* @__PURE__ */ d.jsxs("div", { className: "risk-level", "data-level": Ts(y.uncertainty), children: [
        /* @__PURE__ */ d.jsx("span", { className: "label", children: "Risk Assessment" }),
        /* @__PURE__ */ d.jsx("span", { className: "value", children: y.risk_assessment || "Unknown" })
      ] }),
      /* @__PURE__ */ d.jsxs("div", { className: "investigation-status", children: [
        /* @__PURE__ */ d.jsxs("div", { className: "investigated", children: [
          /* @__PURE__ */ d.jsx("h4", { children: "✅ Investigated" }),
          /* @__PURE__ */ d.jsx("ul", { children: y.investigated.map((R) => /* @__PURE__ */ d.jsx("li", { children: R }, R)) })
        ] }),
        y.not_investigated && y.not_investigated.length > 0 && /* @__PURE__ */ d.jsxs("div", { className: "not-investigated", children: [
          /* @__PURE__ */ d.jsx("h4", { children: "⚠️ Not Investigated" }),
          /* @__PURE__ */ d.jsx("ul", { children: y.not_investigated.map((R) => /* @__PURE__ */ d.jsx("li", { children: R }, R)) })
        ] })
      ] })
    ] }),
    s.length > 0 && /* @__PURE__ */ d.jsxs("div", { className: "files-section", children: [
      /* @__PURE__ */ d.jsx("h3", { children: "Files Changed" }),
      /* @__PURE__ */ d.jsx("div", { className: "files-list", children: s.map((R) => /* @__PURE__ */ d.jsxs("div", { className: "file-item", children: [
        /* @__PURE__ */ d.jsxs("div", { className: "file-name", children: [
          _s(R.status),
          " ",
          R.name
        ] }),
        /* @__PURE__ */ d.jsxs("div", { className: "file-confidence", children: [
          /* @__PURE__ */ d.jsx("div", { className: "confidence-bar", children: /* @__PURE__ */ d.jsx(
            "div",
            {
              className: "confidence-fill",
              style: {
                width: `${R.confidence * 100}%`,
                backgroundColor: js(R.confidence)
              }
            }
          ) }),
          /* @__PURE__ */ d.jsxs("span", { className: "confidence-value", children: [
            (R.confidence * 100).toFixed(0),
            "%"
          ] })
        ] })
      ] }, R.name)) })
    ] }),
    /* @__PURE__ */ d.jsx("div", { className: "session-info", children: /* @__PURE__ */ d.jsxs("p", { className: "small-text", children: [
      "Analyzed by: ",
      /* @__PURE__ */ d.jsx("strong", { children: y.ai_id }),
      " | Session: ",
      /* @__PURE__ */ d.jsxs("code", { children: [
        y.session_id.substring(0, 8),
        "..."
      ] }),
      " | Confidence Basis: ",
      /* @__PURE__ */ d.jsx("em", { children: y.confidence_basis })
    ] }) })
  ] });
};
function Ts(e) {
  return e < 0.2 ? "low" : e < 0.5 ? "medium" : "high";
}
function js(e) {
  return e >= 0.9 ? "#22c55e" : e >= 0.7 ? "#eab308" : e >= 0.5 ? "#f97316" : "#ef4444";
}
function _s(e) {
  switch (e) {
    case "added":
      return "✨";
    case "modified":
      return "📝";
    case "deleted":
      return "🗑️";
    default:
      return "📄";
  }
}
function Cs(e) {
  return "modified";
}
const As = "empirica-epistemic-insight", Ns = "1.0.0", Qs = (e) => (console.log("Initializing Empirica Epistemic Insight Plugin", e), {
  name: As,
  version: Ns,
  config: e || {}
});
export {
  Zs as CommitInsight,
  Es as ConfidenceBadge,
  vs as EmpericaClient,
  Ss as LearningDelta,
  Os as VerificationBadge,
  Qs as initializePlugin,
  As as pluginName,
  Ns as pluginVersion
};
//# sourceMappingURL=empirica-plugin.es.js.map
