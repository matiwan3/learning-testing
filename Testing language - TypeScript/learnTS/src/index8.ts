type Draggale = {
    drag: () => void
};

type Resizable = {
    resize: () => void
};

type UIWidget = Draggale & Resizable;

let textBox: UIWidget = {
    drag: () => {},
    resize: () => {}
}