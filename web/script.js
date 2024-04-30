const canvas = new fabric.Canvas('canvas', {
    backgroundColor: 'lightgray',
    selection: false
});

canvas.setWidth(window.innerWidth * 0.8);
canvas.setHeight(window.innerHeight * 0.8);
canvas.renderAll();

// Добавление зума и перетаскивания
canvas.on('mouse:wheel', function(opt) {
    var delta = opt.e.deltaY;
    var zoom = canvas.getZoom();
    zoom *= 0.999 ** delta;
    if (zoom > 20) zoom = 20;
    if (zoom < 0.01) zoom = 0.01;
    canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);
    opt.e.preventDefault();
    opt.e.stopPropagation();
});

canvas.on('mouse:down', function(opt) {
    var evt = opt.e;
    if (evt.altKey === true) {
        this.isDragOn = true;
        this.selection = false;
        this.lastPosX = evt.clientX;
        this.lastPosY = evt.clientY;
    }
});

canvas.on('mouse:move', function(opt) {
    if (this.isDragOn) {
        var e = opt.e;
        this.viewportTransform[4] += e.clientX - this.lastPosX;
        this.viewportTransform[5] += e.clientY - this.lastPosY;
        this.requestRenderAll();
        this.lastPosX = e.clientX;
        this.lastPosY = e.clientY;
    }
});

canvas.on('mouse:up', function(opt) {
    this.isDragOn = false;
    this.selection = true;
});
let id = 0;

function addBlock() {
    const rect = new fabric.Rect({
        left: 100,
        top: 100,
        width: 100,
        height: 50,
        fill: 'lightblue',
        stroke: 'blue',
        strokeWidth: 2,
        cornerColor: 'blue',
        transparentCorners: false,
        cornerSize: 10,
        padding: 10,
        lockScalingFlip: true
    });

    const text1 = new fabric.Text('Text 1', {
        fontSize: 16,
        fontFamily: 'Arial',
        textAlign: 'center',
        left: rect.left + rect.width / 2,
        top: rect.top - 20
    });

    const text2 = new fabric.Text('Text 2', {
        fontSize: 16,
        fontFamily: 'Arial',
        textAlign: 'center',
        left: rect.left + rect.width / 2,
        top: rect.top + rect.height + 10
    });

    const group = new fabric.Group([rect, text1, text2], {
        id: id++
    });

    canvas.add(group);
    canvas.setActiveObject(group);
    canvas.renderAll();
}