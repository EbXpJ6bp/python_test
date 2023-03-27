import _convert
import _extract


if __name__ == "__main__":

    # TODO: 利用先の指定(優先度 低)

    # 実験結果のcsvファイルを、セミコロン区切りからカンマ区切りに変換
    _convert.semicolon_to_comma()

    # カンマ区切りのcsvファイルからコインシデンスを抽出
    _extract.hom_interference_experiment_result()