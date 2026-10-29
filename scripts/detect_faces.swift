import Foundation
import Vision
import AppKit

if CommandLine.arguments.count < 2 {
    fputs("Usage: swift detect_faces.swift <image_paths...>\n", stderr)
    exit(1)
}

for path in CommandLine.arguments.dropFirst() {
    guard let image = NSImage(contentsOfFile: path),
          let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path)\tERROR: Cannot load image")
        continue
    }
    let req = VNDetectFaceRectanglesRequest()
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([req])
        let faces = (req.results ?? []).map { obs -> String in
            let b = obs.boundingBox
            return String(format: "%.4f,%.4f,%.4f,%.4f", b.origin.x, b.origin.y, b.size.width, b.size.height)
        }
        print("\(path)\t\(faces.joined(separator: ";"))")
    } catch {
        print("\(path)\tERROR: \(error)")
    }
}
