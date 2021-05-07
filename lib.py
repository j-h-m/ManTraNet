def read_rgb_image( image_file ) :
    rgb = cv2.imread( image_file, 1 )[...,::-1]
    return rgb
    
def decode_an_image_array( rgb, manTraNet ) :
    x = np.expand_dims( rgb.astype('float32')/255.*2-1, axis=0 )
    t0 = datetime.now()
    y = manTraNet.predict(x)[0,...,0]
    t1 = datetime.now()
    return y, t1-t0

def decode_an_image_file( image_file, manTraNet ) :
    rgb = read_rgb_image( image_file )
    mask, ptime = decode_an_image_array( rgb, manTraNet )
    return rgb, mask, ptime.total_seconds()

def slice_and_decode(filename, manTraNet):
    tiles = image_slicer.slice(filename, number_tiles=6)
    mask_tiles = []
    total_ptime = 0
    for tile in tiles:
        rgb, mask, ptime = decode_an_image_file(tile.filename, manTraNet)
        mask_image = Image.fromarray(np.uint8(mask * 255))
        mask_tile = image_slicer.Tile(image=mask_image, number=tile.number, position=tile.position, coords=tile.coords)
        mask_tiles.append(mask_tile)
        total_ptime += ptime
    mask_tiles = tuple(mask_tiles)
    res = image_slicer.join(mask_tiles)
    return res, total_ptime