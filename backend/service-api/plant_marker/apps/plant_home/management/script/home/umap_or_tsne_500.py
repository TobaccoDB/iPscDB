import pandas as pd
import os

base_dir = '.'


def Cell_Id_Format(cell_id):
    return str(cell_id).replace("@", ".")


def umap_data(num):
    # 读取 Umap_location 数据
    umap_location_path = os.path.join(base_dir, "umap_data_old.csv")
    umap_location_data = pd.read_csv(umap_location_path)
    umap_location_number = len(umap_location_data)
    print(umap_location_number)
    umap_cell_type_list = list(set(umap_location_data['Cell_type'].values.tolist()))
    umap_location_last_data = pd.DataFrame()
    # sample_umap_len = int(num/len(umap_cell_type_list))
    for cell_type in umap_cell_type_list:
        cell_type_every_data = umap_location_data[umap_location_data['Cell_type'] == cell_type]
        cell_type_every_data_len = len(cell_type_every_data)

        cell_type_len = int((cell_type_every_data_len / umap_location_number) * num)
        print(cell_type_len)
        if cell_type_every_data_len < cell_type_len:
            cell_type_every_data = cell_type_every_data.sample(n=cell_type_every_data_len)
        else:
            cell_type_every_data = cell_type_every_data.sample(n=cell_type_len)
        umap_location_last_data = pd.concat([umap_location_last_data, cell_type_every_data])

    print(umap_location_last_data)
    umap_location_last_data['Cell_ID'] = umap_location_last_data['Cell_ID'].apply(Cell_Id_Format)
    umap_location_last_data.to_csv(f'{base_dir}/umap_data.csv', index=False)


def tsne_data(num):
    # 读取 tsne_data 数据
    tsne_location_path = os.path.join(base_dir, "tsne_data_old.csv")
    tsne_location_data = pd.read_csv(tsne_location_path)
    tsne_location_number = len(tsne_location_data)
    print(tsne_location_number)
    tsne_cell_type_list = list(set(tsne_location_data['Cell_type'].values.tolist()))
    tsne_location_last_data = pd.DataFrame()
    # sample_tsne_len = int(num/len(tsne_cell_type_list))

    for cell_type in tsne_cell_type_list:
        cell_type_every_data = tsne_location_data[tsne_location_data['Cell_type'] == cell_type]
        cell_type_every_data_len = len(cell_type_every_data)
        cell_type_len = int((cell_type_every_data_len / tsne_location_number) * num)

        if cell_type_every_data_len < cell_type_len:
            cell_type_every_data = cell_type_every_data.sample(n=cell_type_every_data_len)
        else:
            cell_type_every_data = cell_type_every_data.sample(n=cell_type_len)

        tsne_location_last_data = pd.concat([tsne_location_last_data, cell_type_every_data])

    print(tsne_location_last_data)
    # 保存数据
    tsne_location_last_data['Cell_ID'] = tsne_location_last_data['Cell_ID'].apply(Cell_Id_Format)
    tsne_location_last_data.to_csv(f'{base_dir}/tsne_data.csv', index=False)


if __name__ == "__main__":
    num = 20000
    umap_data(num)
    tsne_data(num)
